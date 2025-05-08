using Renci.SshNet;
using System.Collections.Generic;
using System;
using System.Text.Json;
using MySqlConnector;

public class DBManager
{
    public static int getUserEcopoints(int user_id)
    {
        using var command = new MySqlCommand($"SELECT ecopoints FROM test_carbon_cruncher.user WHERE user_id='{user_id}'");
        using var reader = command.ExecuteReader();
        int ecopoints = reader.GetInt32(0);
        return ecopoints;
    }

    public static bool setUserEcopoints(int user_id, int ecopoints)
    {
        using var command = new MySqlCommand($"UPDATE test_carbon_cruncher.user SET ecopoints='{ecopoints}' WHERE user_id='{user_id}'");
        int rows = command.ExecuteNonQuery();
        return rows > 0;
    }

    public static string getUserGameData(int user_id)
    {
        using var command = new MySqlCommand($"SELECT gamedata FROM test_carbon_cruncher.user WHERE user_id='{user_id}'");
        using var reader = command.ExecuteReader();
        string game_data_json = reader.GetString(0);
        return game_data_json;
    }

    public static bool setUserGameData(int user_id, string game_data_json)
    {
        using var command = new MySqlCommand($"UPDATE test_carbon_cruncher.user SET game_data='{game_data_json}' WHERE user_id='{user_id}'");
        int rows = command.ExecuteNonQuery();
        return rows > 0;
    }

    public static MySqlConnection dbConnect()
    {
        var sshServer = "79.72.72.89:22";
        var sshUserName = "ubuntu";
        var sshKeyFile = "server.key";
        var databaseServer = "10.0.1.31:3306";
        var databaseUserName = "appclient";
        var databasePassword = "CSC2033client!";

        var (sshClient, localPort) = ConnectSsh(sshServer, sshUserName, sshKeyFile: sshKeyFile, databaseServer: databaseServer);
        using (sshClient)
        {
            MySqlConnectionStringBuilder csb = new MySqlConnectionStringBuilder
            {
                Server = "127.0.0.1",
                Port = localPort,
                UserID = databaseUserName,
                Password = databasePassword,
            };

            using var connection = new MySqlConnection(csb.ConnectionString);
            connection.Open();
            return connection;
        }

    }

    public static (SshClient SshClient, uint Port) ConnectSsh(string sshHostName, string sshUserName, string sshPassword = null,
        string sshKeyFile = null, string sshPassPhrase = null, int sshPort = 22, string databaseServer = "localhost", int databasePort = 3306)
        {
            // check arguments
            if (string.IsNullOrEmpty(sshHostName))
                throw new ArgumentException($"{nameof(sshHostName)} must be specified.", nameof(sshHostName));
            if (string.IsNullOrEmpty(sshHostName))
                throw new ArgumentException($"{nameof(sshUserName)} must be specified.", nameof(sshUserName));
            if (string.IsNullOrEmpty(sshPassword) && string.IsNullOrEmpty(sshKeyFile))
                throw new ArgumentException($"One of {nameof(sshPassword)} and {nameof(sshKeyFile)} must be specified.");
            if (string.IsNullOrEmpty(databaseServer))
                throw new ArgumentException($"{nameof(databaseServer)} must be specified.", nameof(databaseServer));

            // define the authentication methods to use (in order)
            var authenticationMethods = new List<AuthenticationMethod>();
            if (!string.IsNullOrEmpty(sshKeyFile))
            {
                authenticationMethods.Add(new PrivateKeyAuthenticationMethod(sshUserName,
                    new PrivateKeyFile(sshKeyFile, string.IsNullOrEmpty(sshPassPhrase) ? null : sshPassPhrase)));
            }
            if (!string.IsNullOrEmpty(sshPassword))
            {
                authenticationMethods.Add(new PasswordAuthenticationMethod(sshUserName, sshPassword));
            }

            // connect to the SSH server
            var sshClient = new SshClient(new ConnectionInfo(sshHostName, sshPort, sshUserName, authenticationMethods.ToArray()));
            sshClient.Connect();

            // forward a local port to the database server and port, using the SSH server
            var forwardedPort = new ForwardedPortLocal("127.0.0.1", databaseServer, (uint)databasePort);
            sshClient.AddForwardedPort(forwardedPort);
            forwardedPort.Start();

            return (sshClient, forwardedPort.BoundPort);
        }

}