/**
 * @file Main.java
 * @brief Displays main screen and starts up objects for the inventory.
 * @author Jake Schwarz
 */
package com.company;

import javax.swing.*;


public class Main
{
    public static void main(String[] args)  throws Exception{

        // Create objects
        Player player = new Player();
        JFrame app = new JFrame("Inventory Simulator");
        Inventory inventory = new Inventory( app, player );

        // Connect to the database
        inventory.connect_to_inv_db();

        // Add sample items to the inventory
        inventory.add_item(1);
        inventory.add_item(2);
        inventory.add_item(3);
        inventory.add_item(4);
        inventory.add_item(5);
        inventory.add_item(2);

        // Setup window
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setSize(880,700);
        app.setLayout(null);
        app.setVisible(true);

        // Open inventory
        inventory.access_inventory();

        // Reset the window
        app.setVisible(false);
        app.dispose();
    }


}
