/**
 * @file Events.java
 * @brief Runs through various encounters
 * @author Alex Neargarder
 */
package com.company;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.sql.*;
import java.util.*;

import static java.lang.Thread.sleep;

public class Events
{

    //public final static int TOTAL_EVENT_NUMBER = 15;
    //int answer;
    //boolean continueEvent = false;
    //boolean skip_tut = false;

    // Event numbers that have special meaning
    public final static int RANDOM_EVENT = -2;
    public final static int EXIT_GAME = -1;
    public final static int GAME_OVER = 0;
    public final static int TUTORIAL_START = 1;
    public final static int FIRST_BOSS = 71;
    public final static int FINAL_BOSS = 74;

    public static Events inst;

    JFrame app;
    Player player;
    Inventory inventory;
    Combat combat;
    Shop shop;
    int lastReceivedItem;

    //Logbook variables
    Item[] items = new Item[30];
    Statement s;
    String descrip;
    JLabel[] itemsj = new JLabel[10];
    JButton[] icons = new JButton[10];
    int selected_item = -1;
    Connection conns;
    Connection enemies;
    Statement ss;


    // Possible random events
    ArrayList<Integer> eventNumbers;
    ArrayList<Integer> permanentNumbers;
    Random rand;

    // Database
    Connection conn;
    Statement db;

    // Used in displayChoices()
    String decisionString;
    boolean continueEvent;

    public Events( JFrame app, Player player, Inventory inventory )
    {
        this.app = app;
        this.player = player;
        this.inventory = inventory;
        shop = new Shop( app, inventory, this );
        rand = new Random();
        inst = this;

        try
        {
            conn = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
            db = conn.createStatement();
        }
        catch (SQLException e)
        {
            e.printStackTrace();
        }

        combat = new Combat( inventory, app, player, this, conn, db);

        // Load in all potential random events
        eventNumbers = new ArrayList<>();
        permanentNumbers = new ArrayList<>();

        try
        {
            String q = "Select Event_ID from EVENTS where Is_start=1";
            ResultSet r = db.executeQuery(q);

            while ( r.next() )
            {
                eventNumbers.add( r.getInt(1) );
            }

            // Any events with allow_multiple set to true will be saved in a separate
            // array so we know not to remove them
            q = "Select Event_ID from EVENTS where Is_start=1 AND Allow_Multiple=1";
            r = db.executeQuery(q);

            while ( r.next() )
            {
                permanentNumbers.add( r.getInt(1) );
            }
        }
        catch ( SQLException ex )
        {
            ex.printStackTrace();
        }

        continueEvent = false;

    }

    // Returns a randomly selected event
    int getRandomEvent()
    {
        if ( eventNumbers.size() == 0 )
        {
            return 0;
        }

        int chosen = rand.nextInt( eventNumbers.size() );

        if ( !permanentNumbers.contains( eventNumbers.get(chosen) ) )
        {
            return eventNumbers.remove( chosen );
        }
        else
        {
            return eventNumbers.get(chosen);
        }
    }

    // Returns true for continue, false for exit
    boolean displayIntermission()
    {
        int decision = displayChoices("You have a moment to catch your breath.",
                "Exit", "Open Inventory", "Logbook", "Continue");

        do
        {
            // Return 0 to play the game over screen
            if ( decision == 1 )
            {
                return false;
            }
            // Open inventory
            else if ( decision == 2 )
            {
                inventory.access_inventory();
            }
            else if ( decision == 3)
            {
                display_logbook();
            }
            else
            {
                break;
            }

            decision = displayChoices("You have a moment to catch your breath.",
                    "Exit", "Open Inventory","Logbook", "Continue");
        }
        while ( decision != 4 );

        return true;
    }

    // Main game loop
    public void start()
    {
        int nextEvent = TUTORIAL_START;

        int playCount = 0;

        while ( nextEvent != EXIT_GAME )
        {
            // First check if game over should be displayed
            if ( nextEvent == GAME_OVER )
            {
                nextEvent = playEvent(nextEvent);
            }
            // First boss after 5 events
            else if ( playCount == 5 )
            {
                nextEvent = playEvent( FIRST_BOSS );
            }
            // Final boss after 11 events
            else if ( playCount == 11 )
            {
                nextEvent = playEvent( FINAL_BOSS );
            }
            // Random event
            else if ( nextEvent == RANDOM_EVENT )
            {
                nextEvent = getRandomEvent();
                nextEvent = playEvent( nextEvent );
            }
            // This should only happen for the tutorial probably
            else
            {
                nextEvent = playEvent( nextEvent );
            }

            if ( nextEvent != EXIT_GAME && !displayIntermission() )
            {
                nextEvent = GAME_OVER;
            }

            ++playCount;

            // Unlock a new spell every 2 events
            if ( playCount % 2 == 0 )
            {
                ++player.currentSpells.lastUnlocked;
            }
            inventory.tick_down_duration();
        }
    }

    void checkRequires( Map< Integer, String > hm, String require )
    {
        if ( require == null || require.equals("") )
        {
            return;
        }

        String[] tokens = require.split(";");
        String[] command;
        String[] items;
        boolean commandEval;

        for (String token : tokens )
        {
            // Remove whitespace at the beginning and end
            token = token.trim();

            // Split the command into 3 parts
            command = token.split(" ");
            // Split the comma-separated items into an array
            items = command[2].split(",");

            boolean requirebool = true;

            if ( command[1].equals("REQUIRENOT") )
            {
                requirebool = false;
            }

            commandEval = true;
            // Check if the inventory contains each item listed
            for ( int i = 0; i < items.length; ++i )
            {
                if ( items[i].equals("WEAPON") )
                {
                    if ( inventory.has_weapon_equipped() != requirebool )
                    {
                        commandEval = false;
                    }
                }
                else if ( (inventory.check_inventory_id_exists( Integer.parseInt( items[i] ) ) == -1) == requirebool )
                {
                    commandEval = false;
                    break;
                }
            }

            // Command evaluated to false so the option needs to be removed
            if ( !commandEval )
            {
                hm.remove( Integer.parseInt( command[0] ) );
            }

        }
    }

    String checkForPrints( String text )
    {
        text = text.replace("PRINTCOINS", inventory.get_inv_coins() + "" );
        if ( text.contains("PRINTITEM") )
            text = text.replace( "PRINTITEM", inventory.get_item_from_db(lastReceivedItem).name );

        return text;
    }

    // Executes a single command
    int executeCommand( String[] command, int nextEvent )
    {
        boolean result = true;

        // Handle each possible command
        if ( command[0].equals("ADDITEM") )
        {
            if ( command[1].equals("RANDOM") )
            {
                lastReceivedItem = inventory.get_random_item();
                inventory.add_item( lastReceivedItem );
            }
            else
            {
                lastReceivedItem = Integer.parseInt( command[1] );
                inventory.add_item( lastReceivedItem );
            }
        }
        else if ( command[0].equals("REMOVEITEM") )
        {
            inventory.remove_item_id( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("ADDHP") )
        {
            player.increase_hp( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("LOSEHP") )
        {
            player.decrease_hp( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("EQUIPWEAPON") )
        {
            inventory.equip_weapon( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("EQUIPARMOR") )
        {
            inventory.equip_armor( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("GOTO") )
        {
            if ( command[1].equals("RANDOM") )
            {
                nextEvent = RANDOM_EVENT;
            }
            else
            {
                nextEvent = Integer.parseInt( command[1] );
            }
        }
        else if ( command[0].equals("FIGHT") )
        {
            if ( command[1].equals("RANDOM") )
            {
                Enemy enemy = new Enemy( -1 );

                result = combat.engage_combat( enemy );
            }
            else
            {
                Enemy enemy = new Enemy( Integer.parseInt(command[1]) );

                result = combat.engage_combat( enemy );
            }
        }
        else if ( command[0].equals("ADDCOINS") )
        {
            inventory.coin_purse.add_coins( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("REMOVECOINS") )
        {
            inventory.coin_purse.subtract_coins( 10 );
        }
        else if ( command[0].equals("SHOP") )
        {
            if ( command[1].equals("RANDOM") )
            {
                shop.start_shop( inventory.get_random_item(), inventory.get_random_item(), inventory.get_random_item() );
            }
            else
            {
                String[] items = command[1].split(",");

                shop.start_shop( Integer.parseInt(items[0]),
                        Integer.parseInt(items[1]), Integer.parseInt(items[2]) );
            }
        }
        // GET indicates command is a conditional
        else if ( command[0].contains("GET") )
        {
            int value = 0;
            if ( command[0].equals("GETCOINS") )
            {
                value = inventory.get_inv_coins();
            }
            else if ( command[0].equals("GETSTRENGTH") )
            {
                value = player.STRENGTH;
            }
            // Generate random number 0 - 99
            else if ( command[0].equals("GETRAND") )
            {
                value = rand.nextInt(100);
            }

            if ( command[1].equals(">") )
            {
                result = value > Integer.parseInt(command[2]);
            }
            else if ( command[1].equals("<") )
            {
                result = value < Integer.parseInt(command[2]);
            }
            else if ( command[1].equals("==") )
            {
                result = value == Integer.parseInt(command[2]);
            }
        }
        else if ( command[0].equals("INCREASESTRENGTH") )
        {
            player.increase_strength( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("INCREASEDEFENSE") )
        {
            player.increase_defense( Integer.parseInt(command[1]) );
        }
        else if ( command[0].equals("HASITEM") )
        {
            result = inventory.check_inventory_id_exists( Integer.parseInt(command[1]) ) != -1;
        }
        else if ( command[0].equals("HASNOTITEM") )
        {
            result = inventory.check_inventory_id_exists( Integer.parseInt(command[1]) ) == -1;
        }
        else if ( !command[0].equals("") )
        {
            System.out.println("WARNING UNRECOGNIZED COMMAND: " + command[0]);
        }

        // Check for ternary operator
        for ( int i = 0; i < command.length; ++i )
        {
            if ( command[i].equals("?") )
            {
                if ( result )
                {
                    String[] option1 = { command[i+1], command[i+2] };
                    nextEvent = executeCommand( option1, nextEvent );
                }
                else
                {
                    String[] option2 = { command[i+4], command[i+5] };
                    nextEvent = executeCommand( option2, nextEvent );
                }
            }
        }

        return nextEvent;
    }

    // Executes a list of commands
    int executeActions( String actions )
    {
        if ( actions == null || actions.equals("") )
        {
            return EXIT_GAME;
        }

        String[] tokens = actions.split(";");
        String[] command;
        String[] items;
        int nextEvent = EXIT_GAME;

        for ( String token : tokens )
        {
            // Remove leading / trailing whitespace
            token = token.trim();
            command = token.split(" ");

            //System.out.println("command: " + command[0]);
            //System.out.println("argument: " + command[1]);

            nextEvent = executeCommand( command, nextEvent );
        }

        return nextEvent;
    }

    boolean continue_log = true;
    int log_accessed = 0;
    int results = 0;
    void display_logbook() {
        continue_log = true;
        app.getContentPane().removeAll();
        log_accessed = 1;


        JLabel description_box = new JLabel("Search the logbook by ID or name");
        description_box.setBounds(200, 10, 500, 85);
        description_box.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
        description_box.setHorizontalAlignment(JTextField.CENTER);



        try
        {
            conns = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
            s = conns.createStatement();
        }
        catch (SQLException e)
        {
            e.printStackTrace();
        }
        JLabel label_box = new JLabel("Search for items");
        label_box.setBounds(250, 130, 200, 40);
        JTextField search_text = new JTextField();
        search_text.setBounds(200, 100, 200, 40);
        search_text.addActionListener(new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent e) {
                for(int i = 0; i < results; i++){
                    app.remove(icons[i]);
                    app.remove(itemsj[i]);

                }
                results = 0;

                descrip = search_text.getText();

                String q = "Select * from ITEMS where item_id = '" + descrip + "' OR item_name LIKE '%" + descrip + "%' COLLATE NOCASE";
                ResultSet r;
                Item item = new Item();
                try {
                    r = s.executeQuery(q);
//                System.out.println(r);
                    while(r.next())
                    {

                    Item tmp = new Item();
                    tmp.item_id = r.getInt(1);
                    tmp.name = r.getString(2);
                    tmp.description = r.getString(3);
                    tmp.type = r.getInt(4);

                    tmp.effect = r.getInt(5);
                    tmp.affected_stat = r.getInt(6);
                    tmp.duration = r.getInt(7);
                    tmp.value = r.getInt(8);
                    tmp.quantity = r.getInt(9);
                    tmp.img = r.getString(10);
                    if(tmp.item_id != 13 && tmp.item_id != 14) {
                        item = tmp;

                        items[results] = item;
                        results++;
                    }
                    }if(results == 0){
                        description_box.setText("No Results Found");
                    }else{
                        description_box.setText("Select an Item to view its information.");
                    }
                } catch (SQLException f) {
                    description_box.setText("No Results Found");
                    f.printStackTrace();
                }


                for (int i = 0; i < results; i++) {
                    itemsj[i] = new JLabel();
                    Border border = BorderFactory.createLineBorder(Color.GRAY, 1);
                    itemsj[i].setHorizontalAlignment(SwingConstants.CENTER);
                    itemsj[i].setVerticalAlignment(JLabel.TOP);
                    if (i > 3)
                        itemsj[i].setBounds(40 + ((i % 4) * 180), 275, 180, 100);
                    else
                        itemsj[i].setBounds(40 + (i * 180), 175, 180, 100);
                    itemsj[i].setBorder(border);
                }

                for (int i = 0; i < results; i++) {
                    icons[i] = new JButton();

                    if (i > 3)
                        icons[i].setBounds(100 + ((i % 4) * 180), 300, 64, 64);
                    else
                        icons[i].setBounds(100 + (i * 180), 200, 64, 64);
                }

                for (int i = 0; i < results; i++) {
                    itemsj[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                }
                show_log(itemsj, icons, description_box);
                app.repaint();


            }
        });








        try
        {
            enemies = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
            ss = enemies.createStatement();
        }
        catch (SQLException g)
        {
            g.printStackTrace();
        }

        JLabel label_boxe = new JLabel("Search for enemies");
        label_boxe.setBounds(550, 130, 200, 40);
        JTextField search_texte = new JTextField();
        search_texte.setBounds(500, 100, 200, 40);
        search_texte.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                for(int i = 0; i < results; i++){
                    app.remove(icons[i]);
                    app.remove(itemsj[i]);

                }
                results = 0;
                descrip = search_texte.getText();
                String q = "Select * from ENEMIES where Enemy_ID = '" + descrip + "' OR Name LIKE '%" + descrip + "%' COLLATE NOCASE";
                ResultSet r;
                ResultSet d;


                try {
                    r = ss.executeQuery(q);
                    int e_id = r.getInt(1);
                    String enemy_details = "<html>Enemy ID: " + e_id + "<BR>Enemy Name: " + r.getString(5) + "<BR>HP: " + r.getInt(3) + "<BR>Damage: " + r.getInt(4);
                    if(r.getInt(1) != 2){
                        int enemy_id = r.getInt(1);
                        String q2 = "Select * from DROPS where Enemy_ID='" + enemy_id + "'";
                        d = ss.executeQuery(q2);
                        int drops[] = {d.getInt(3), d.getInt(4), d.getInt(5)};
                        for (int i = 0; i < 3; i++){
                            if (e_id == 8){
                                enemy_details = enemy_details + "<BR>Drops: Any Item";
                                break;
                            }
                            else if (e_id == 9 || e_id == 10){
                                enemy_details = enemy_details + "<BR>Drops: Coins";
                                break;
                            }
                            if(drops[i] != 0){
                                if(i == 0)
                                    enemy_details = enemy_details + "<BR>Drops: ";
    //                                System.out.println("Drop" + (i+1) + ": " + drops[i]);
                                String q3 = "select item_name from ITEMS, DROPS where item_id" + (i+1) + "=item_id and " + "enemy_id=" + enemy_id;
                                ResultSet dr = ss.executeQuery(q3);
    //                                System.out.println("Drop" + (i+1) + ": " + dr.getString("item_name"));
                                if (i < 2 && drops[i+1] != 0)
                                    enemy_details = enemy_details + dr.getString("item_name") + ", ";
                                else
                                    enemy_details = enemy_details + dr.getString("item_name");
                            }
                        }
//                        System.out.println("Drop1: " + d.getInt(2) + "\n" + "Drop2: " + d.getInt(3) + "\n" + "Drop2: " + d.getInt(4));
                        enemy_details = enemy_details + "</html>";
                        description_box.setText(enemy_details);
                    }
                } catch (SQLException f) {
                    description_box.setText("No Results Found");
                    //f.printStackTrace();
                }

                app.repaint();
            }
        });
        app.add(search_texte);
        app.add(search_text);
        app.add(label_box);
        app.add(label_boxe);





        JButton exit = new JButton("Exit Logbook");
        exit.setBounds(100, 600, 300, 40);
        exit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                app.getContentPane().removeAll();
                continue_log = false;
            }
        });


        //show_log(itemsj, icons);

        app.add(description_box);
        app.add(exit);
        app.repaint();

        try
        {
            while (continue_log)
            {
                sleep(100);
            }
        }
        catch (InterruptedException ex)
        {
            ex.printStackTrace();
        }
        continue_log = true;


    }

    private void show_log( JLabel[] itemsj, JButton[] icons, JLabel description_box)
    {

        for (int i = 0; i < results; i++){

//            icons[i] = new JButton();
//
//            if(i > 4)
//                icons[i].setBounds(100+((i%5)*180), 225, 64, 64);
//            else
//                icons[i].setBounds(100+(i*180), 125, 64, 64);
            BufferedImage image = null;
            try
            {
                String image_name = items[i].img;
//                switch (items[i].item_id) {
//                    case 1:
//                        image_name = "RustySword.png";
//                        break;
//                    case 2:
//                        image_name = "MinorHealingPotion.png";
//                        break;
//                    case 4:
//                        image_name = "LeatherArmor.png";
//                        break;
//                    case 5:
//                        image_name = "Torch.png";
//                        break;
//                    case 8:
//                        image_name = "IronArmor.png";
//                        break;
//                    case 10:
//                        image_name = "IronSword.png";
//                        break;
//                    default:
//                        image_name = "TestSquare.png";
//                        break;
//                }
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
                    for (int i = 0; i < results; i++)
                        itemsj[i].setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
                    selected_item = finalI;
                    itemsj[finalI].setBorder(BorderFactory.createLineBorder(Color.BLUE, 1));
                    description_box.setText("<html>Item ID: " + items[finalI].item_id + "<BR>Item Name: " + items[finalI].name + "<BR>Value: " + items[finalI].value + "<BR>Description: " + items[finalI].description + "</html>");


            }
            });
        }

        String[] shown_inv = new String[10];
        if(items.length != 0)
        {
            for (int i = 0; i < results; i++)
            {
                    shown_inv[i] = items[i].name;

            }
        }

        for (int i = 0; i < results; i++){
            app.add(itemsj[i]);
            app.add(icons[i]);
            itemsj[i].setText(shown_inv[i]);
        }


    }

    int playEvent( int eventNum )
    {
        String q = "Select * from EVENTS where Event_ID=" + eventNum;
        ResultSet r;
        Map< Integer, String > temp = new LinkedHashMap< Integer, String >();
        Map< Integer, String > choices = new LinkedHashMap< Integer, String >();
        Map< Integer, String > results = new LinkedHashMap< Integer, String >();

        String preactions = "", story = "", require = "";

        try
        {
            r = db.executeQuery(q);

            preactions = r.getString( 5 );
            story = r.getString( 6 );
            temp.put( 1, r.getString( 7 ) );
            temp.put( 2, r.getString( 8 ) );
            temp.put( 3, r.getString( 9 ) );
            temp.put( 4, r.getString( 10 ) );
            temp.put( 5, r.getString( 11 ) );
            require = r.getString( 12 );
            results.put( 1, r.getString( 13 ) );
            results.put( 2, r.getString( 14 ) );
            results.put( 3, r.getString( 15 ) );
            results.put( 4, r.getString( 16 ) );
            results.put( 5, r.getString( 17 ) );

            //System.out.println("event description: " + r.getString(2 ));
//            System.out.println("preactions: " + preactions);
//            System.out.println("story: " + story);
//            System.out.println("choice1: " + temp.get(1) );
//            System.out.println("choice2: " + temp.get(2) );
//            System.out.println("choice3: " + temp.get(3) );
//            System.out.println("choice4: " + temp.get(4) );
//            System.out.println("choice5: " + temp.get(5) );
//            System.out.println("require: " + require);
//            System.out.println("result1: " + results.get(1) );
//            System.out.println("result2: " + results.get(2) );
//            System.out.println("result3: " + results.get(3) );
//            System.out.println("result4: " + results.get(4) );
//            System.out.println("result5: " + results.get(5) );
        }
        catch ( SQLException ex )
        {
            ex.printStackTrace();
        }

        executeActions( preactions );

        // Look at the require string and remove and options which don't meet the required conditions
        checkRequires( temp, require );

        // Remove any options that are null or empty
        for ( Map.Entry< Integer, String > entry : temp.entrySet() )
        {
            if ( entry.getValue() != null && !entry.getValue().equals("") )
            {
                choices.put( entry.getKey(), entry.getValue() );
                //System.out.println("option " + entry.getKey() + ": " + entry.getValue());
            }
        }

        // Replace any text in the story text that is a print command
        story = checkForPrints( story );

        //System.out.println();

//        for ( String choice : choices.values().toArray(new String[0]))
//        {
//            System.out.println("option: " + choice);
//        }

        String[] choicesArray = choices.values().toArray(new String[0]);

        int decision = displayChoices( story, choicesArray );

        for ( Map.Entry< Integer, String > entry : choices.entrySet() )
        {
            if ( entry.getValue().equals( choicesArray[decision - 1] ) )
            {
                decision = entry.getKey();
                break;
            }
        }

        //System.out.println( "executing action: " + results.get(decision) );

        eventNum = executeActions( results.get(decision) );

        //System.out.println("next event: " + eventNum);

        if ( eventNum >= 0 )
        {
            eventNum = playEvent( eventNum );
        }

        return eventNum;
    }

    // optionStrings is an array of strings whose length depends on how many arguments are
    // passed to this function
    int displayChoices(String storyText, String ...optionStrings)
    {
        app.getContentPane().removeAll(); //Clears everything currently on screen
        app.setLayout(new BoxLayout(app.getContentPane(), BoxLayout.PAGE_AXIS) );

        JLabel story = new JLabel("<html>" + storyText + "</html>");
        story.setMaximumSize( new Dimension(500, 500));
        Border border = BorderFactory.createLineBorder(Color.GRAY, 1);
        story.setBorder(border);

        ArrayList<JButton> optionButtons = new ArrayList<>();
        JButton option;

        for ( int i = 0; i < optionStrings.length; ++i )
        {
            option = new JButton(optionStrings[i]);
            option.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    decisionString = e.getActionCommand(); // This gets the text of the button that was pressed
                    continueEvent = true;
                }
            });
            optionButtons.add( option );
        }


        JPanel storyPanel = new JPanel();
        storyPanel.setLayout(new BoxLayout(storyPanel, BoxLayout.LINE_AXIS));
        storyPanel.add(story);
        JPanel optionsPanel = new JPanel( new FlowLayout() );

        for ( JButton x : optionButtons )
        {
            optionsPanel.add(x);
        }

        app.add(storyPanel);
        app.add( Box.createVerticalStrut( 80 ) );
        app.add(optionsPanel);
        app.repaint();

        try {
            while (!continueEvent) {
                Thread.sleep(100);
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }

        continueEvent = false;

        app.setLayout(null);

        for ( int i = 0; i < optionStrings.length; ++i )
        {
            if ( optionStrings[i].equals( decisionString ) )
            {
                return i + 1;
            }
        }

        return -1;
    }

    int displayCombat(String storyText, String option1Text, String option2Text, Enemy enemy) {
        app.getContentPane().removeAll(); //Clears everything currently on screen

        app.setLayout(new BoxLayout(app.getContentPane(), BoxLayout.PAGE_AXIS) );

        JLabel description_box = new JLabel("<html>" + "Click an image followed by a button to use the inventory." + "</html>");
        description_box.setMaximumSize( new Dimension(500, 80));
        Border border = BorderFactory.createLineBorder(Color.GRAY, 1);
        description_box.setBorder(border);

        JPanel descriptionPanel = new JPanel();
        descriptionPanel.setLayout(new BoxLayout(descriptionPanel, BoxLayout.LINE_AXIS));
        descriptionPanel.setBorder(border);
        JPanel optionsPanel = new JPanel( new FlowLayout() );

        JLabel story = new JLabel("<html>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + storyText + "</html>");
//        Border border = BorderFactory.createLineBorder(Color.GRAY, 1);
//        story.setBounds(100, 100, 500, 100);
//        story.setBorder(border);

       /* JLabel currentHP = new JLabel();
        currentHP.setBounds(20, 0, 100, 40);*/

        JButton option1 = new JButton(option1Text);
        option1.setBounds(100, 400, 300, 40);
        option1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                decisionString = e.getActionCommand(); // This gets the text of the button that was pressed
                continueEvent = true;
            }
        });

        JButton option2 = new JButton(option2Text);
        option2.setBounds(400,400,300,40);
        option2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                decisionString = e.getActionCommand(); // This gets the text of the button that was pressed
                continueEvent = true;
            }
        });

        JButton option3 = new JButton("Spells");
        option3.setBounds(100,500,300,40);
        option3.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                decisionString = e.getActionCommand(); // This gets the text of the button that was pressed
                continueEvent = true;
            }
        });

        JButton option4 = new JButton("Open Inventory");
        option4.setBounds(400,500,300,40);
        option4.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                decisionString = e.getActionCommand(); // This gets the text of the button that was pressed
                continueEvent = true;
            }
        });

        JLabel Hp = new JLabel();
        Hp.setMaximumSize( new Dimension(50, 30));
        Hp.setHorizontalAlignment(JTextField.CENTER);
        descriptionPanel.add(Hp);

//        Hp.setBounds(20,0,100,40);

        JLabel Mana = new JLabel();
        Mana.setBorder(border);
        Mana.setMaximumSize( new Dimension(50, 30));
//        Mana.setBounds(20,20,100,40);

        JLabel E_Hp = new JLabel();
        E_Hp.setBorder(border);
        E_Hp.setMaximumSize( new Dimension(50, 30));
//        E_Hp.setBounds(20, 40, 400, 40);

        Hp.setText("<html>  HP = <font color='2ccb38'>" + player.HP + "  </font></html>");
        Mana.setText("<html>  Mana = <font color='1e99d7'>" + player.currentMana + "  </font></html>");
        E_Hp.setText("<html>  " + enemy.name + "'s HP = <font color='ff0000'>" + enemy.HP + "  </font></html>");
        if(enemy.HP < 0)
        {
            E_Hp.setText(enemy.name + " = 0");
        }

        descriptionPanel.add(Hp);
        descriptionPanel.add(Mana);
        descriptionPanel.add(E_Hp);

        descriptionPanel.add(story);
//        app.add(option1);
//        app.add(option2);
//        app.add(option3);
//        app.add(option4);
        optionsPanel.add(option1);
        optionsPanel.add(option2);
        optionsPanel.add(option3);
        optionsPanel.add(option4);

        description_box.setHorizontalAlignment(JTextField.CENTER);
        app.add(descriptionPanel);

        app.add( Box.createVerticalStrut( 80 ) );
        app.add(optionsPanel);
        /*app.add(currentHP);
        currentHP.setText("HP = " + player.HP));*/
        app.repaint();

        try {
            while (!continueEvent) {
                Thread.sleep(100);
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }

        continueEvent = false;

        if ( option1Text.equals(decisionString) )
            return 1;
        else if ( option2Text.equals(decisionString) )
            return 2;
        else if ( "Spells".equals(decisionString) )
            return 3;
        else if ( "Open Inventory".equals(decisionString) )
            return 4;
        else
            return -1;
    }

}

