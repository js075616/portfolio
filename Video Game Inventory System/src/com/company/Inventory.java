/**
 * @file Inventory.java
 * @brief Contains all the necessary functions to control inventory.
 * @author Jake Schwarz
 */

package com.company;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.Locale;
import java.util.Random;

import static java.lang.Thread.sleep;

public class Inventory
{
    Item[] inv = new Item[10]; //array of Item objects
    Item[] active_items = new Item[3]; //array for three active items that go away after duration equals 0
    Item weapon_equipslot = new Item(); //current equipped weapon
    Item armor_equipslot = new Item(); //current equipped armor
    Coins coin_purse = new Coins(); //creates a new Coins object
    int next_slot = 0; //next available index for an item
    int next_active = 0; //next available active item
    JLabel[] invs = new JLabel[10]; //items in the inventory
    JButton[] icons = new JButton[10]; //images for the inventory items
    JFrame app; //application
    Player player; //player object
    int inv_accessed = 0; //check if the inventory has been accessed before
    boolean continue_inv = true; //loop to continue accessing inventory
    int selected_item = -1; //current selected item
    Connection conn; //connection to database
    Statement s; //statement to be passed to the database

    /**
     * @brief Get the objects from Main.java.
     * @param app The main app window.
     * @param player The player from the main app.
     */
    public Inventory( JFrame app, Player player ) {
        this.app = app;
        this.player = player;
    }

    /**
     * @brief Connects to the database. Makes an exception if it does not work.
     */
    public void connect_to_inv_db(){
        try {
            conn = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
            s = conn.createStatement();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * @brief Checks if the inventory is empty.
     * @return Returns if the inventory is empty.
     */
    public boolean inventory_empty() { return next_slot == 0;}

    /**
     * @brief Checks to see if a weapon is equipped.
     * @return If there is a weapon.
     */
    public boolean has_weapon_equipped() { return weapon_equipslot.item_id != 0; }

    /**
     * @brief Checks to see if an armor is equipped.
     * @return If there is an armor.
     */
    public boolean has_armor_equipped() { return armor_equipslot.item_id != 0; }


    /**
     * @brief Controls inventory management by adding or removing items. Also initializes information for the inventory.
     */
    public void access_inventory() {

        app.getContentPane().removeAll();

        inv_accessed = 1;

        app.getContentPane().removeAll(); //Clears everything currently on screen
        app.setLayout(new BoxLayout(app.getContentPane(), BoxLayout.PAGE_AXIS) );

        JLabel description_box = new JLabel("<html>" + "Click an image followed by a button to use the inventory." + "</html>");
        description_box.setMaximumSize( new Dimension(500, 80));
        Border border = BorderFactory.createLineBorder(Color.GRAY, 1);
        description_box.setBorder(border);

        JPanel descriptionPanel = new JPanel();
        descriptionPanel.setLayout(new BoxLayout(descriptionPanel, BoxLayout.LINE_AXIS));
        JPanel optionsPanel = new JPanel( new FlowLayout() );
        JPanel disPanel = new JPanel( new FlowLayout() );
        JPanel itemsPanel = new JPanel( new FlowLayout() );

        for (int i = 0; i < next_slot; i++) {
            invs[i] = new JLabel();
            border = BorderFactory.createLineBorder(Color.GRAY, 1);
            invs[i].setHorizontalAlignment(SwingConstants.CENTER);
            invs[i].setVerticalAlignment(JLabel.TOP);
            if (i > 4)
                invs[i].setBounds(40 + ((i % 5) * 180), 200, 180, 100);
            else
                invs[i].setBounds(40 + (i * 180), 100, 180, 100);
            invs[i].setBorder(border);
        }
//
        for (int i = 0; i < next_slot; i++) {
            icons[i] = new JButton();

            if (i > 4)
                icons[i].setBounds(100 + ((i % 5) * 180), 225, 64, 64);
            else
                icons[i].setBounds(100 + (i * 180), 125, 64, 64);
        }
//
        JLabel Hp = new JLabel();
        Hp.setBorder(border);
//        Hp.setBounds(20, 0, 100, 40);

        JLabel Str = new JLabel();
        Str.setBorder(border);
//        Str.setBounds(20, 20, 100, 40);

        JLabel Def = new JLabel();
        Def.setBorder(border);
//        Def.setBounds(20, 40, 100, 40);

        JLabel coins = new JLabel();
        coins.setBorder(border);
//        coins.setBounds(20, 60, 100, 40);

        Hp.setMaximumSize( new Dimension(50, 30));
        Hp.setHorizontalAlignment(JTextField.CENTER);
        descriptionPanel.add(Hp);

        Str.setMaximumSize( new Dimension(80, 30));
        Str.setHorizontalAlignment(JTextField.CENTER);
        descriptionPanel.add(Str);

        Def.setMaximumSize( new Dimension(80, 30));
        Def.setHorizontalAlignment(JTextField.CENTER);
        descriptionPanel.add(Def);

        coins.setMaximumSize( new Dimension(80, 30));
        coins.setHorizontalAlignment(JTextField.CENTER);
        descriptionPanel.add(coins);

        descriptionPanel.add(description_box);
        description_box.setHorizontalAlignment(JTextField.CENTER);
        app.add(descriptionPanel);
        app.add( Box.createVerticalStrut( 40 ) );

        JButton des_btn = new JButton("Show Description");
//        optionsPanel.add( des_btn );
//        des_btn.setBounds(100, 350, 300, 40);
        des_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                description_box.setText("Click the item you wish to know more about");
                app.repaint();
                if (selected_item > -1 && selected_item <= next_slot) {
                    description_box.setText(inv[selected_item].description);
                } else {
                    description_box.setText("Not an item.");
                }
                for (int i = 0; i < next_slot; i++)
                    invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                app.repaint();
                selected_item = -1;
            }
        });

        JButton wea_btn = new JButton("Equip Weapon");
//        optionsPanel.add( wea_btn );
//        wea_btn.setBounds(100, 400, 300, 40);
        wea_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selected_item > -1 && selected_item <= next_slot && inv[selected_item].type == 1) {
                    if (has_weapon_equipped() == false) {
                        description_box.setText(inv[selected_item].name + " equipped.");
//                        player.increase_strength(inv[selected_item].effect);
                    } else {
                        description_box.setText(weapon_equipslot.name + " " + "swapped with " + inv[selected_item].name);
                    }
                    equip_weapon(selected_item);
                } else {
                    description_box.setText("Not a weapon.");
                }
                show_inventory(invs, icons, itemsPanel);
                if (!check_inventory_type("Weapon")) {
                    optionsPanel.remove(wea_btn);
                }
                Str.setText("<html>Strength = <font color='9a3636'>" + player.STRENGTH + "</font></html>");
                for (int i = 0; i < next_slot; i++)
                    invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                app.repaint();
                selected_item = -1;
            }
        });

        JButton arm_btn = new JButton("Equip Armor");
//        optionsPanel.add(arm_btn );
//        arm_btn.setBounds(100, 450, 300, 40);
        arm_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selected_item > -1 && selected_item <= next_slot && inv[selected_item].type == 2) {
                    if (has_armor_equipped() == false) {
                        description_box.setText(inv[selected_item].name + " equipped.");
                    } else {
                        description_box.setText(armor_equipslot.name + " " + "swapped with " + inv[selected_item].name);
                    }
                    equip_armor(selected_item);
                } else {
                    description_box.setText("Not an armor.");
                }
                show_inventory(invs, icons, itemsPanel);
                for (int i = 0; i < next_slot; i++)
                    invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                if (!check_inventory_type("Armor")) {
                    optionsPanel.remove(arm_btn);
                }
                Def.setText("<html>Defense = <font color='8a18c4'>" + player.DEFENSE + "</font></html>");
                app.repaint();
                selected_item = -1;
            }
        });

        JButton use_btn = new JButton("Use Item");
//        optionsPanel.add( use_btn );
//        use_btn.setBounds(100, 500, 300, 40);
        use_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (next_active < 3) {
                    if (selected_item > -1 && selected_item < next_slot && inv[selected_item].type == 3) {
                        if (inv[selected_item].affected_stat == 1 && inv[selected_item].item_id == 11) {
                            description_box.setText(inv[selected_item].name + " used.");
                        } else {
                            description_box.setText(inv[selected_item].name + " now active.");
                        }
                        use_item(selected_item);
                    }
//                    else if(use_int == 11)
//                    {
//                        description_box.setText("God Mode Activated.");
//                        use_item(selected_item , player);
//                    }
                    else {
                        description_box.setText("Not a usable item.");
                    }
                    show_inventory(invs, icons, itemsPanel);
                    if (!check_inventory_type("Potion")) //&& !check_inventory_type("Utility"))
                    {
                        optionsPanel.remove(use_btn);
                    }
                    Hp.setText("<html>HP = <font color='2ccb38'>" + player.HP + "</font></html>");
                    Def.setText("<html>Defense = <font color='8a18c4'>" + player.DEFENSE + "</font></html>");
                    Str.setText("<html>Strength = <font color='9a3636'>" + player.STRENGTH + "</font></html>");
                } else {
                    description_box.setText("You cannot use another active item.");
                }
                Hp.setText("<html>HP = <font color='2ccb38'>" + player.HP + "</font></html>");
                Def.setText("<html>Defense = <font color='8a18c4'>" + player.DEFENSE + "</font></html>");
                Str.setText("<html>Strength = <font color='9a3636'>" + player.STRENGTH + "</font></html>");
                for (int i = 0; i < next_slot; i++)
                    invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                app.repaint();
                selected_item = -1;
            }
        });

        disPanel.add(new JLabel("Confirm: "));
        JButton discard_conf_btn = new JButton("Yes");
//        discard_conf_btn.setBounds(450, 550, 100, 40);
        disPanel.add( discard_conf_btn );
        JButton discard_deny_btn = new JButton("No");
//        discard_deny_btn.setBounds(600, 550, 100, 40);
        disPanel.add( discard_deny_btn );
        discard_conf_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selected_item > -1 && selected_item <= next_slot) {
                    description_box.setText(inv[selected_item].name + " discarded.");
                    remove_item((selected_item));
                    show_inventory(invs, icons, itemsPanel);
                    for (int i = 0; i < next_slot; i++)
                        invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    description_box.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    if (!check_inventory_type("Weapon")) //&& !check_inventory_type("Utility"))
                    {
                        optionsPanel.remove(wea_btn);
                    }
                    if (!check_inventory_type("Armor")) //&& !check_inventory_type("Utility"))
                    {
                        optionsPanel.remove(arm_btn);
                    }
                    if (!check_inventory_type("Potion")) //&& !check_inventory_type("Utility"))
                    {
                        optionsPanel.remove(use_btn);
                    }
                    app.repaint();
                    selected_item = -1;
                }
//                app.remove(discard_conf_btn);
//                app.remove(discard_deny_btn);
                app.remove(disPanel);
            }
        });

        discard_deny_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selected_item > -1 && selected_item <= next_slot) {
                    description_box.setText(inv[selected_item].name + " was not discarded.");
                    show_inventory(invs, icons, itemsPanel);
                    for (int i = 0; i < next_slot; i++)
                        invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    description_box.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    app.repaint();
                    selected_item = -1;
                }
//                app.remove(discard_conf_btn);
//                app.remove(discard_deny_btn);
                app.remove(disPanel);
            }
        });

        JButton discard_btn = new JButton("Discard Item");
//        optionsPanel.add( discard_btn );
//        discard_btn.setBounds(100, 550, 300, 40);
        discard_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selected_item > -1 && selected_item <= next_slot) {
                    description_box.setText("Are you sure you want to discard " + inv[selected_item].name + "?");
                    description_box.setBorder(BorderFactory.createLineBorder(Color.RED, 2));
//                    disPanel.add(discard_conf_btn);
//                    disPanel.add(discard_deny_btn);
                    app.add(disPanel);
                    app.repaint();
                } else {
                    description_box.setText("Not an item.");
                }
                for (int i = 0; i < next_slot; i++)
                    invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                app.repaint();
            }
        });

        JButton exit = new JButton("Exit Inventory");
//        optionsPanel.add( exit );
//        exit.setBounds(100, 600, 300, 40);
        exit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                app.getContentPane().removeAll();
                continue_inv = false;
            }
        });
//
        Hp.setText("<html>HP = <font color='2ccb38'>" + player.HP + "</font></html>");
        Str.setText("<html>Strength = <font color='9a3636'>" + player.STRENGTH + "</font></html>");
        Def.setText("<html>Defense = <font color='8a18c4'>" + player.DEFENSE + "</font></html>");
        coins.setText("<html>Coins = <font color='d4af37'>" + coin_purse.get_coins()+ "</font></html>");
//        app.add(description_box);
        show_inventory(invs, icons, itemsPanel);
        app.add(itemsPanel);
        optionsPanel.add(des_btn);
        if (check_inventory_type("Weapon")) {
            optionsPanel.add(wea_btn);
        }
        if (check_inventory_type("Armor")) {
            optionsPanel.add(arm_btn);
        }
        if (check_inventory_type("Potion"))//|| check_inventory_type("Utility"))
        {
            optionsPanel.add(use_btn);
        }
        optionsPanel.add(discard_btn);
        optionsPanel.add(exit);
        app.add(optionsPanel);
//        descriptionPanel.setMaximumSize( descriptionPanel.getPreferredSize() );
//        itemsPanel.setMaximumSize( itemsPanel.getPreferredSize() );
//        optionsPanel.setMaximumSize( optionsPanel.getPreferredSize() );
//        disPanel.setMaximumSize(disPanel.getPreferredSize());
//        app.add(Hp);
//        app.add(Str);
//        app.add(Def);
//        app.add(coins);
        //app.add(test);
        app.repaint();

        try
        {
            while (continue_inv)
            {
                sleep(100);
            }
        }
        catch (InterruptedException ex)
        {
            ex.printStackTrace();
        }
        continue_inv = true;
    }

    /**
     * @brief Grabs an item's information from the database.
     * @param item_id ID of the item to be retrieved.
     * @return An item object with the information from the database.
     */
    public Item get_item_from_db(int item_id){
        String q = "Select * from ITEMS where item_id = " + item_id;
        ResultSet r;
        Item item = new Item();
        try {
            r = s.executeQuery(q);
//                System.out.println(r);
            Item tmp = new Item();
            tmp.item_id = r.getInt(1);
            tmp.name = r.getString(2);
            tmp.description = r.getString(3);
            tmp.type = r.getInt(4);
//                    System.out.println("/" + tmp.type +"/");
            tmp.effect = r.getInt(5);
            tmp.affected_stat = r.getInt(6);
            tmp.duration = r.getInt(7);
            tmp.value = r.getInt(8);
            tmp.quantity = r.getInt(9);
            tmp.img = r.getString(10);
            item = tmp;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return item;
    }

    /**
     * @brief Adds a new item to the inventory.
     * @param item_id Id of the item to be added to the inventory
     */
    public void add_item(int item_id)
    {
        if(next_slot < 10)
        {
            if(check_inventory_id_exists(item_id) != -1)
            {
                inv[check_inventory_id_exists(item_id)].increase_quantity();
            }
            else{
                Item tmp = get_item_from_db(item_id);
                inv[next_slot] = tmp;
                next_slot++;
            }
        }
        else
        {
            System.out.println("Inventory Full.");
        }
    }

    /**
     * @brief Removes an item from the array. Shifts all array items back to remove it.
     * @param slot Index number of item to be removed.
     */
    public void remove_item(int slot)
    {
        if(inv[slot].quantity > 1)
        {
            inv[slot].decrease_quantity();
            //System.out.println("Quantity of " + inv[slot].name + " decreased by 1.");
        }
        else
            {
            //System.out.println(inv[slot].name + " was removed.");
            if(inv_accessed == 1){
                app.remove(icons[next_slot-1]);
                app.remove(invs[next_slot-1]);
                app.revalidate();
            }
            next_slot--;
            for (int i = slot; i < next_slot; i++) {
                inv[i] = inv[i + 1];
            }
        }
    }

    /**
     * @brief Removes an item from the inventory based on an ID.
     * @param item_id ID of the item to be removed.
     */
    public void remove_item_id(int item_id)
    {
        int r_slot = -1;
        for(int i = 0; i < next_slot; i++)
        {
            if(inv[i].item_id == item_id)
            {
                r_slot = i;

            }
        }
        if(r_slot != -1)
        {
            if(inv[r_slot].quantity > 1)
            {
                inv[r_slot].decrease_quantity();
            }
            else
            {
                for (int j = r_slot; j < next_slot; j++) {
                    inv[j] = inv[j + 1];
                }
                next_slot--;
            }
        }
        else
        {
            System.out.println("Item does not exist.");
        }
    }

    /**
     * @brief Lists all items in the inventory, as well as the current equipped weapon and armor. Also shows coins.
     * @param invs Item names in the inventory.
     * @param icons Images for the items. Act as buttons to select items.
     * @param itemsPanel JPanel that contains all the item names and images.
     */
    private void show_inventory( JLabel[] invs, JButton[] icons, JPanel itemsPanel )
    {
        for (int i = 0; i < next_slot; i++){

//            icons[i] = new JButton();
//
//            if(i > 4)
//                icons[i].setBounds(100+((i%5)*180), 225, 64, 64);
//            else
//                icons[i].setBounds(100+(i*180), 125, 64, 64);
            BufferedImage image = null;
            try
            {
                String image_name = inv[i].img;
                String fs = File.separator;
                File imageFile = new File( "src" + fs + "com" + fs + "company" + fs + "assets" + fs + image_name );
                if ( !imageFile.exists() )
                {
                    System.out.println("WARNING: " + imageFile.getAbsolutePath() + " doesn't exist");
                    image = ImageIO.read( new File( "src" + fs + "com" + fs + "company" + fs + "assets" + fs + "TestSquare.png" ) );
                }
                else
                {
                    image = ImageIO.read(imageFile);
                }
            }
            catch (Exception e)
            {
                e.printStackTrace();
                System.exit(1);
            }

            ImageIcon testicon = new ImageIcon(image);
            icons[i].setIcon(testicon);
            int finalI = i;
            icons[i].setBorderPainted(false);
            icons[i].setContentAreaFilled(false);
            for( ActionListener al :icons[i].getActionListeners() ) {
                icons[i].removeActionListener( al );
            }
            icons[i].addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
//                    System.out.print(inv[finalI].type);
                    for (int i = 0; i < next_slot; i++)
                        invs[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    selected_item = finalI;
                    invs[finalI].setBorder(BorderFactory.createLineBorder(Color.BLUE, 1));
//                    System.out.println(selected_item);
                }
            });
        }

        String[] shown_inv = new String[10];
        if(inventory_empty() == false)
        {
            for (int i = 0; i < next_slot; i++)
            {
                if(inv[i].quantity > 1)
                {
                    shown_inv[i] = i + 1 + ". " + inv[i].name + " x" + inv[i].quantity;
                }
                else
                {
                    shown_inv[i] = i + 1 + ". " + inv[i].name;
                }
            }
        }
        itemsPanel.removeAll();
        itemsPanel.revalidate();
        itemsPanel.repaint();

        for (int i = 0; i < next_slot; i++){
            itemsPanel.add(invs[i]);
            itemsPanel.add(icons[i]);
            invs[i].setText(shown_inv[i]);
        }

        app.repaint();
    }

    /**
     * @brief Checks if the inventory array contains a type of item.
     * @param check_type The item type that is being checked.
     * @return If the inventory contains the type.
     */
    public boolean check_inventory_type(String check_type) /* Changed to public */
    {
        boolean check = false;
        int type = 0;
        if (check_type == "Weapon")
            type = 1;
        if (check_type == "Armor")
            type = 2;
        if (check_type == "Potion")
            type = 3;
        if (check_type == "Utility")
            type = 4;
        for (int i = 0; i < next_slot; i++)
        {
//            System.out.println("Comparing " + check_type + " with " + inv[i].type);
            if(inv[i].type == type)
            {
                check = true;
                break;
            }
        }
        return check;
    }

    /**
     * @brief Checks if the inventory contains a specific item. Currently unused.
     * @param item_check The id of the item to be found.
     * @return The index of the item if it is within the inventory.
     */
    public int check_inventory_id_exists(int item_check)
    {
        for (int i = 0; i < next_slot; i++)
        {
            if(inv[i].item_id == item_check)
            {
                return i;
            }
        }
        return -1;
    }

    /**
     * @brief Equips the weapon into weapon_equipslot
     * @param slot Slot of the weapon to be equipped.
     */
    public void equip_weapon(int slot)
    {
        if(check_inventory_type("Weapon") == true)
        {
            if (inv[slot].type == 1)
            {
                if (weapon_equipslot.item_id == 0)
                {
                    weapon_equipslot = inv[slot];
                    remove_item(slot);
                    player.increase_strength(weapon_equipslot.effect);
//                    System.out.println(weapon_equipslot.name + " equipped.");
                }
                else
                    {
                        player.decrease_strength(weapon_equipslot.effect);
                    Item tmp = new Item();
                    tmp = weapon_equipslot;
                    weapon_equipslot = inv[slot];
                    inv[slot] = tmp;
                    player.increase_strength(weapon_equipslot.effect);
//                    System.out.println(tmp.name + " swapped with " + weapon_equipslot.name);
                }
            }
            else
                {
                System.out.println("Not a Weapon.");
            }

        }
        else
        {
            System.out.println("Can't equip a weapon.");
        }
    }

    /**
     * @brief Equips the armor into armor_equipslot
     * @param slot Slot of the armor to be equipped.
     */
    public void equip_armor(int slot) {
        if (check_inventory_type("Armor") == true)
        {
            if (inv[slot].type == 2)
            {
                if (armor_equipslot.item_id == 0)
                {
                    armor_equipslot = inv[slot];
                    remove_item(slot);
                    player.increase_defense(armor_equipslot.effect);
//                    System.out.println(armor_equipslot.name + " equipped.");
                }
                else
                    {
                        player.decrease_defense(armor_equipslot.effect);
                    Item tmp = new Item();
                    tmp = armor_equipslot;
                    armor_equipslot = inv[slot];
                    inv[slot] = tmp;
                    player.increase_defense(armor_equipslot.effect);
                    System.out.println(tmp.name + " swapped with " + armor_equipslot.name);
                }
            }
            else
                {
                System.out.println("Not an Armor.");
            }
        }
        else
        {
            System.out.println("Can't equip an armor.");
        }
    }

    /**
     * @brief Buys the requested item, adds it to the inventory, and removes the value of the item from coins.
     * @param new_id Id of the item to be bought.
     */
    public void buy_item(int new_id)
    {
        Item tmp_item2 = get_item_from_db(new_id);
        if(coin_purse.get_coins() >= tmp_item2.value) {
            add_item(new_id);
            coin_purse.subtract_coins(tmp_item2.value);
        }
        else
        {
            System.out.println("Not enough coins.");
        }
    }

    /**
     * @brief Uses an item from the inventory, such as a potion.
     * @param slot The index of the item to be used.
     */
    private void use_item(int slot)
    {
        if(slot == 10)
        {
            player.increase_hp(99);
            player.increase_strength(99);
            player.increase_defense(99);
        }
        else if(next_active < 3)
        {
            if(inv[slot].affected_stat == 1)
            {
                player.increase_hp(inv[slot].effect);
                remove_item(slot);
            }
            else if(inv[slot].type == 3 && inv[slot].affected_stat != 1)
            {
                active_items[next_active] = inv[slot];
                if(active_items[next_active].affected_stat == 2)
                {
                    player.increase_strength(active_items[next_active].effect);
                }
                if(active_items[next_active].affected_stat == 3)
                {
                    player.increase_defense(active_items[next_active].effect);
                }
                if(active_items[next_active].affected_stat == 4)
                {
                    player.recoverMana(active_items[next_active].effect);
                }
                remove_item(slot);
                if(active_items[next_active].duration == 0)
                {
                    for (int i = next_active; i < next_active; i++) {
                        active_items[i] = active_items[i + 1];
                    }
                    next_active--;
                }
                next_active++;
            }
            else
            {
                System.out.println("Can't be an active item.");
            }
        }
        else
        {
            System.out.println("No more space for active items.");
        }
    }

    /**
     * @brief Checks to see if a certain item is active.
     * @param item_id ID of item to be checked.
     * @return If the item is active/used or not.
     */
    public boolean has_item_active(int item_id)
    {
        for(int i = 0; i < next_active; i++)
        {
            if(active_items[i].item_id == item_id)
            {
                return true;
            }
        }
        return false;
    }

    /**
     * @brief Reduces the duration of all active items and removes them if no longer active.
     */
    public void tick_down_duration()
    {
        for(int i = 0; i < next_active; i++)
        {
            active_items[i].duration--;
            if(active_items[i].duration == 0)
            {
                if(active_items[i].effect == 2)
                {
                    player.decrease_strength(active_items[i].effect);
                }
                if(active_items[i].effect == 3)
                {
                    player.decrease_defense(active_items[i].effect);
                }
                for (int j = i; j < next_active; j++) {
                    active_items[j] = active_items[j + 1];
                }
                next_active--;
            }
        }
    }

    /**
     * @brief Increases the duration of all active items.
     */
    public void tick_up_duration()
    {
        for(int i = 0; i < next_active; i++)
        {
            active_items[i].duration++;
        }
    }
}

