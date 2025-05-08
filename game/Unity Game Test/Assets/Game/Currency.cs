using UnityEngine;
using TMPro;

public class Currency : MonoBehaviour

{
    public TextMeshProUGUI ePointText;
    readonly int ecoPoints = 0;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {   
        // Displays current users eco points
        ePointText.text = "EcoPoints: " + ecoPoints.ToString(); 
    }

}

