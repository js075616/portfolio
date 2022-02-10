/**
 * @file Item.java
 * @brief Variables and methods necessary for an Item object.
 * @author Jake Schwarz
 */

package com.company;

public class Item {
    int type;
    String description;
    int effect; //could be damage, defense, etc.
    int affected_stat; //1 - HP, 2 - STRENGTH, 3 - DEFENSE
    int item_id;
    int value;
    int duration;
    int quantity;
    String name;
    String img;

    /**
     * @brief Default constructor for Item objects.
     */
    Item()
    {
        type = 0;
        description = "Default";
        effect = 0;
        affected_stat = 0;
        item_id = 0;
        value = 0;
        duration = 0;
        quantity = 0;
        name = "Default";
        img = "testsquare.png";
    }

    /**
     * @brief Copy constructor for Item objects.
     */
    Item(Item input)
    {
        type = input.type;
        description = input.description;
        effect = input.effect;
        affected_stat = input.affected_stat;
        item_id = input.item_id;
        value = input.value;
        duration = input.duration;
        quantity = input.quantity;
        name = input.name;
        img = input.img;
    }

    public void increase_quantity()
    {
        quantity++;
    }

    public void decrease_quantity()
    {
        quantity--;
    }

//    /**
//     * @brief Looks up the information on an item. Contains all available items.
//     * @param lookup_id Id of an item to be looked up.
//     * @return An Item object with the new information and variables.
//     */
//    public Item item_set_info(int lookup_id)
//    {
//        Item tmp = new Item();
//        switch (lookup_id)
//        {
//            case 0:
//                tmp.type = 2;
//                tmp.name = "T-51b Power Armor";
//                tmp.description = "Mysterious armor from a far away time and place. Very heavy, but provides 7 defense.";
//                tmp.effect = 7;
//                tmp.value = 30;
//                tmp.quantity = 1;
//                tmp.item_id = 0;
//                break;
//
//            case 1:
//                tmp.type = 1;
//                tmp.name = "Rusty Sword";
//                tmp.description = "Ancient, well used sword. Deals 2 damage.";
//                tmp.effect = 2;
//                tmp.value = 1;
//                tmp.quantity = 1;
//                tmp.item_id = 1;
//                break;
//
//            case 2:
//                tmp.type = 3;
//                tmp.name = "Minor Healing Potion";
//                tmp.description = "Heals HP by 10";
//                tmp.effect = 10;
//                tmp.affected_stat = 1;
//                tmp.value = 5;
//                tmp.quantity = 1;
//                tmp.item_id = 2;
//                break;
//
//            case 3:
//                tmp.type = 1;
//                tmp.name = "Iron Dagger";
//                tmp.description = "Small dagger made of iron. Deals 4 damage.";
//                tmp.effect = 4;
//                tmp.value = 5;
//                tmp.quantity = 1;
//                tmp.item_id = 3;
//                break;
//
//            case 4:
//                tmp.type = 2;
//                tmp.name = "Leather Armor";
//                tmp.description = "Weak armor made of cow's leather. Provides 2 defense.";
//                tmp.effect = 2;
//                tmp.value = 10;
//                tmp.quantity = 1;
//                tmp.item_id = 4;
//                break;
//
//            case 5:
//                tmp.type = 4;
//                tmp.name = "Torch";
//                tmp.description = "Lights up a dark room. 1 Use.";
//                tmp.value = 3;
//                tmp.quantity = 1;
//                tmp.item_id = 5;
//                break;
//
//            case 6:
//                tmp.type = 3;
//                tmp.name = "Minor Strength Potion";
//                tmp.description = "Lasts 3 events. Increases STRENGTH by 2";
//                tmp.effect = 2;
//                tmp.affected_stat = 2;
//                tmp.duration = 3;
//                tmp.value = 10;
//                tmp.quantity = 1;
//                tmp.item_id = 6;
//                break;
//
//            case 7:
//                tmp.type = 3;
//                tmp.name = "Minor Defense Potion";
//                tmp.description = "Lasts 3 events. Increases DEFENSE by 2";
//                tmp.effect = 2;
//                tmp.affected_stat = 3;
//                tmp.duration = 3;
//                tmp.value = 10;
//                tmp.quantity = 1;
//                tmp.item_id = 7;
//                break;
//
//            case 8:
//                tmp.type = 2;
//                tmp.name = "Iron Armor";
//                tmp.description = "Stronger armor made of fine iron, with twice the defense of leather. Provides 4 defense.";
//                tmp.effect = 4;
//                tmp.value = 20;
//                tmp.quantity = 1;
//                tmp.item_id = 8;
//                break;
//
//            case 9:
//                tmp.type = 4;
//                tmp.name = "Bronze Key";
//                tmp.description = "Unlocks a bronze lock. 1 Use.";
//                tmp.value = 5;
//                tmp.quantity = 1;
//                tmp.item_id = 9;
//                break;
//
//            case 10:
//                tmp.type = 1;
//                tmp.name = "Iron Sword";
//                tmp.description = "A fine sword made by a professional. Deals 5 damage.";
//                tmp.effect = 5;
//                tmp.value = 10;
//                tmp.quantity = 1;
//                tmp.item_id = 10;
//                break;
//
//            case 11:
//                tmp.type = 3;
//                tmp.name = "Holy Hand Grenade";
//                tmp.description = "Deals 999 damage and escapes combat. 1 Use.";
//                tmp.value = 30;
//                tmp.duration = 1;
//                tmp.quantity = 1;
//                tmp.item_id = 11;
//                break;
//
//            case 12:
//                tmp.type = 3;
//                tmp.name = "Healing Potion";
//                tmp.description = "Heals HP by 20";
//                tmp.effect = 20;
//                tmp.affected_stat = 1;
//                tmp.value = 10;
//                tmp.quantity = 1;
//                tmp.item_id = 12;
//                break;
//
//            case 13:
//                tmp.type = 1;
//                tmp.name = "Excalibur";
//                tmp.description = "The legendary sword pulled from the stone. Deals 7 damage.";
//                tmp.effect = 7;
//                tmp.value = 99;
//                tmp.quantity = 1;
//                tmp.item_id = 13;
//                break;
//
//            default:
//                System.out.println("Not an item");
//                break;
//        }
//        return tmp;
//    }
}
