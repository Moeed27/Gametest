using UnityEngine;
using UnityEngine.Tilemaps;

// currentManager - GameManager object
// editMode - Boolean that indicates whether the player is in edit mode or not
// deleteMode - Boolean that indicates whether the player is in delete mode or not
// rotated - Boolean that indicates if a Furniture Game Object has been rotated
// gridLayout - reference to Grid object
// tilemap - reference to main tilemap which displays the room to be decorated
// editTilemap - reference to EditTilemap which shows occupied and unoccupied tiles that the user can place on
// temp - Temporary store of Furniture game object
// prevPos - Stores a Vector3 of the previous position of the temp Furniture game object
public class GameManager : MonoBehaviour

{
    
    public static GameManager currentManager;
    public bool editMode = false;
    public bool deleteMode = false;
    public bool rotated = false;
    public GridLayout gridLayout;
    public Tilemap tilemap;
    public Tilemap editTilemap;
    private Furniture temp;
    private Vector3 prevPos;

    //Creates a game object of furniture (assigned to a button)
    public void InitFurniture(GameObject furniture) {
        deleteMode = false;
        editTilemap.gameObject.SetActive(true);
        temp = Instantiate(furniture, Vector3.zero, Quaternion.identity).GetComponent<Furniture>(); 
    }

    //Checks if the area the game object is currently above is filled with white tiles on main tilemap
    // Returns True if all tiles are white and False otherwise
    public bool ValidArea(BoundsInt area) {
        TileBase[] baseArray = editTilemap.GetTilesBlock(area); //Gets all tiles at position of sprite game object

        // Checks if all tiles specified in baseArray are white
        foreach (var tile in baseArray) {

            // If all tiles are not equal to WhiteTile asset returns false
            if (tile != Resources.Load<Tile>("WhiteTile")) {
                return false;
            }
        }
        
        return true;
    }

  
    //After moving or deleting an object in edit mode, change tiles that the object was previously occupying on the tilemap from red to white
    public void ClearArea(){
        int size = temp.area.size.x * temp.area.size.y * temp.area.size.z;
        TileBase[] tileArray = new TileBase[size];
        for (int i = 0; i < tileArray.Length; i++) {
            tileArray[i] = Resources.Load<TileBase>("WhiteTile");
            print(tileArray[i]);
            
        }
        editTilemap.SetTilesBlock(temp.area, tileArray);
    }

    //When the edit button is pressed, it inverts the boolean value of editMode to indicate whether we are in edit mode or not
    public void InEditMode() {
        deleteMode = false;
        editMode = !editMode;
        if (editMode) {
            editTilemap.gameObject.SetActive(true);
        }
        else {  
            editTilemap.gameObject.SetActive(false);
        }
    }

    //When the delete button is pressed, it inverts the boolean value of deleteMode to indicate whether we are in delete mode or not
    public void InDeleteMode() {
        deleteMode = !deleteMode;
    }

    public void SetTemp(Furniture copy) {
        temp = copy;
    }

    //method that rotates a Furniture game object
    public void Rotate() {
        if (temp != null && temp.Placed == false) {
            Vector3Int tempVector = temp.area.size; 
            Vector3Int invertVector = new(tempVector.y, tempVector.x, tempVector.z);
            temp.area.size = invertVector; //Flips BoundsInt x and y values when flipping

            rotated = !rotated;
            if (rotated) {
                temp.transform.localRotation = Quaternion.Euler(0, 180, 0);
            }
            else{
                temp.transform.localRotation = Quaternion.Euler(0, 0, 0);
            }
        }
        
    } 

    private void Awake() {
        currentManager = this;
    }

    void Update()
    {
        //If furniture object is not initialised then do nothing
        if (!temp) {
            return;
        }

        //If furniture is initialised, attempt to place furniture when clicking
        if(Input.GetMouseButtonDown(0)){
            if (temp.CanBePlaced()) {
                temp.Place();
                rotated = false;
            }
        }

        // if furniture is initalised but not placed, follow mouse cursor
        if(!temp.Placed) {

            Vector2 touchPos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            Vector3Int cellPos = gridLayout.LocalToCell(touchPos);

            if (prevPos != cellPos) {

                temp.transform.localPosition = gridLayout.CellToLocalInterpolated(cellPos + new Vector3(.5f, .5f, 0f));
                prevPos = cellPos;

            }
        }

    }

}
