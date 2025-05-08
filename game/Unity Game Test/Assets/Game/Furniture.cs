using UnityEngine;
using UnityEngine.Tilemaps;
public class Furniture : MonoBehaviour
{
    public bool Placed; //Boolean indicating if game object has been placed on the tilemap
    public BoundsInt area; //Dimension of furniture on tilemap

    private void OnMouseDown(){
        //Delete Furniture
        if (GameManager.currentManager.editMode && GameManager.currentManager.deleteMode && Placed) {
            GameManager.currentManager.ClearArea();
            Furniture copy = Instantiate(this, Vector3.zero, Quaternion.identity).GetComponent<Furniture>(); 
            copy.Placed = false;
            Destroy(gameObject);
            GameManager.currentManager.SetTemp(copy);
            Destroy(copy);
        }
        //Edit Furniture
        else if(GameManager.currentManager.editMode && !GameManager.currentManager.deleteMode && Placed) {
            GameManager.currentManager.ClearArea();
            Furniture copy = Instantiate(this, Vector3.zero, Quaternion.identity).GetComponent<Furniture>(); 
            copy.Placed = false;
            Destroy(gameObject);
            GameManager.currentManager.SetTemp(copy);
        }
    }
    public bool CanBePlaced() {
        Vector3Int position = GameManager.currentManager.gridLayout.LocalToCell(transform.position);
        BoundsInt areaTemp = area;
        areaTemp.position = position;

        if (GameManager.currentManager.ValidArea(areaTemp)) {
            return true;
        }
        return false;
    }

    public void Place() {
        Vector3Int position = GameManager.currentManager.gridLayout.LocalToCell(transform.position);
        BoundsInt areaTemp = area;
        areaTemp.position = position;
        area = areaTemp;
        Placed = true;
        GameManager.currentManager.deleteMode = false;

        //Creates array of tiles where the furniture is placed and paints them red
        int size = areaTemp.size.x * areaTemp.size.y * areaTemp.size.z;
        TileBase[] tileArray = new TileBase[size];

        for (int i = 0; i < tileArray.Length; i++) {
            tileArray[i] = Resources.Load<TileBase>("RedTile");
        }

        GameManager.currentManager.editTilemap.SetTilesBlock(areaTemp, tileArray);

        if (!GameManager.currentManager.editMode) {
            GameManager.currentManager.editTilemap.gameObject.SetActive(false);
        }
    }
}
