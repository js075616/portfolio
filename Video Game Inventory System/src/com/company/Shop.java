/**
 * @file Shop.java
 * @brief Creates a shop where you can buy items
 * @author Jake Schwarz
 */
package com.company;

import javax.swing.*;

public class Shop
{
    JFrame app;
    Inventory inventory;
    Events event;

    public Shop( JFrame app, Inventory inventory, Events event )
    {
        this.app = app;
        this.inventory = inventory;
        this.event = event;
    }

    public void start_shop(int id1, int id2, int id3)
    {
        Item tmp_item = new Item();
        Item item1 = inventory.get_item_from_db(id1);
        Item item2 = inventory.get_item_from_db(id2);
        Item item3 = inventory.get_item_from_db(id3);
        String sitem1 = item1.name + " Cost: " + item1.value;
        String sitem2 = item2.name + " Cost: " + item2.value;
        String sitem3 = item3.name + " Cost: " + item3.value;

        int choice = event.displayChoices("You have arrived at a shop. You can purchase three items. Coins = " + inventory.get_inv_coins(), sitem1, sitem2, sitem3, "Exit shop");

        while(choice != 4)
        {
            switch(choice)
            {
                case 1:
                    if(inventory.get_inv_coins() >= item1.value && sitem1 != "Item bought")
                    {
                        inventory.buy_item(item1.item_id);
                        sitem1 = "Item bought";
                    }
                    else
                    {
                        sitem1 = "Not enough coins.";
                    }
                    break;
                case 2:
                    if(inventory.get_inv_coins() >= item2.value && sitem2 != "Item bought")
                    {
                        inventory.buy_item(item2.item_id);
                        sitem2 = "Item bought";
                    }
                    else
                    {
                        sitem2 = "Not enough coins.";
                    }
                    break;
                case 3:
                    if(inventory.get_inv_coins() >= item3.value && sitem3 != "Item bought")
                    {
                        inventory.buy_item(item3.item_id);
                        sitem3 = "Item bought";
                    }
                    else
                    {
                        sitem3 = "Not enough coins.";
                    }
                    break;
            }
            choice = event.displayChoices("You have arrived at a shop. You can purchase three items. Coins = " + inventory.get_inv_coins(), sitem1, sitem2, sitem3, "Exit shop");
        }
    }
}