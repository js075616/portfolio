/**
 * @file Enemy.java
 * @brief Contains the stats for enemies you may encounter
 * @author Jake Schwarz
 */
package com.company;

import javax.swing.*;
import java.sql.*;
import java.util.Random;

public class Enemy
{
    int HP;
    int damage;
    String name;
    Connection conn;
    Statement db;
    Random rand;

    Enemy( int enemy_number )
    {
        rand = new Random();

        try
        {
            conn = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
            db = conn.createStatement();
        }
        catch (SQLException e)
        {
            e.printStackTrace();
        }

        // Get random enemy
        if ( enemy_number == -1 )
        {
            try
            {
                String q = "Select COUNT(*) from ENEMIES where Allow_Random=1";
                ResultSet r = db.executeQuery(q);

                int count = r.getInt(1);

                q = "Select Enemy_ID from ENEMIES where Allow_Random=1";
                r = db.executeQuery(q);

                count = rand.nextInt(count);

                // Skip first one
                r.next();

                for ( int i = 0; i < count; ++i )
                {
                    r.next();
                }

                enemy_number = r.getInt(1);
            }
            catch ( SQLException ex )
            {
                ex.printStackTrace();
            }
        }

        try
        {
            String q = "Select * from ENEMIES where Enemy_ID=" + enemy_number;
            ResultSet r = db.executeQuery(q);

            this.HP = r.getInt(3);
            this.damage = r.getInt(4);
            this.name = r.getString(5);
        }
        catch ( SQLException ex )
        {
            ex.printStackTrace();
        }
    }



}
