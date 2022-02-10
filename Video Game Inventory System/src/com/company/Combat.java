/**
 * @file Combat.java
 * @brief Handles turn-based combat
 * @author Jake Schwarz
 */
package com.company;

import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;
import java.util.Random;

public class Combat
{
    public static Combat inst;

    boolean chance = false;
    Inventory inventory;
    JFrame app;
    Player player;
    Events events;
    Connection conn;
    Statement db;
    int first_combat = 0;

//    try {
//        conn = DriverManager.getConnection("jdbc:sqlite:src/com/company/databases/encounter.db");
//        s = conn.createStatement();
//    } catch (SQLException e) {
//        e.printStackTrace();
//    }


    public Combat( Inventory inventory, JFrame app, Player player, Events events, Connection conn, Statement db)
    {
        this.inventory = inventory;
        this.app = app;
        this.player = player;
        this.events = events;
        this.inst = this;
        this.conn = conn;
        this.db = db;
    }

    // Returns true if fight ended normally, false if ended via the holy hand grenade
    public boolean engage_combat( Enemy enemy ) {
        String effect = "You engage in combat with the enemy.";
        boolean chance = false;
        boolean end_fight = false;
        int player_damage = 0;
        int enemy_damage = 0;

        int combat_choice = events.displayCombat("You engage in combat with the enemy.", "Attack", "Guard", enemy);
        while(end_fight == false && player.HP > 0 && enemy.HP > 0)
        {
            if(combat_choice == 1)
            {
                player.recoverMana( 1 );
                player_damage = calculate_player_damage(enemy, player);
                enemy_damage = calculate_enemy_damage(enemy, player);
                if(chance == false)
                {
                    enemy.HP -= player_damage;
                    effect = "You dealt " + player_damage + " damage to the " + enemy.name + ". They dealt " + enemy_damage + " to you in retaliation.";
                    player.decrease_hp(enemy_damage);
                }
                else
                {
                    enemy.HP -= player_damage;
                    effect = "You dealt " + player_damage + " damage to the " + enemy.name + ". The " + enemy.name + " missed after being stumbled by your previous guard.";
                    chance = false;
                }
            }
            else if(combat_choice == 2)
            {
                player.recoverMana( 1 );
                player.decrease_hp(enemy_damage/2);
                Random rand = new Random();
                int rand_chance = rand.nextInt(10);
                if(rand_chance < 4)
                {
                    player.decrease_hp(enemy_damage/2);
                    effect = "You guarded, but still took " + enemy_damage / 2 + " damage. The enemy has stumbled and must recover. You have the chance for a free attack.";
                    chance = true;
                }
                else
                {
                    effect = "You guarded, but still took " + enemy_damage / 2 + " damage. The enemy has recovered from your guard.";
                }
            }
            else if(combat_choice == 3)
            {
                int temp = player.currentSpells.displaySpells();

                if ( temp != -1 )
                {
                    effect = player.currentSpells.castSpell( enemy, temp, chance );
                    if ( !effect.equals("Insufficient Mana.") )
                        player.recoverMana( 1 );
                }
            }
            else
            {
                inventory.access_inventory();

                if(inventory.has_item_active(11) == true)
                {
                    end_fight = true;
                    events.displayChoices("You blew the " + enemy.name + " to smithereens.", "Continue");
                    return false;
                }
                else
                {
                    effect = "You continue your fight with the enemy.";
                }
            }
            if(player.HP > 0 && enemy.HP > 0)
            {
                combat_choice = events.displayCombat(effect, "Attack", "Guard", enemy);
            }
            else if(player.HP <= 0)
            {
                int choice = events.displayChoices("Your HP has been reduced to 0. Game Over.", "Exit Game");
                if(choice == 1)
                {
                    app.dispose();
                }
                System.exit(0);
            }
            else if(end_fight == false || enemy.HP <= 0)
            {
               ResultSet r;
               String q = "Select * from DROPS where Enemy_name='" + enemy.name + "'";

                try {
                    r = db.executeQuery(q);
                    int enemy_id = r.getInt(1);
                    int num_items = 0;
                    int drops[] = {r.getInt(3), r.getInt(4), r.getInt(5)};
                    for (int i =0; i < 3; i++){
                        if (drops[i] != 0)
                            num_items++;
                        System.out.println("Drop" + (i+1) + ": " + drops[i]);
                    }
//                    System.out.println(num_items);
                    if(num_items > 1){
                        Random rand = new Random();
//                    System.out.println(enemy_id);
                        int item_num = rand.nextInt((num_items)-1)+1;
                        System.out.println("Picked slot: " + item_num);
                        ResultSet r2;
                        String q2 = "select item_id, item_name from ITEMS, DROPS where item_id" + item_num + "=item_id and " + "enemy_id=" + enemy_id;
                        r2 = db.executeQuery(q2);
                        int itemID = r2.getInt(1);
                        System.out.println("Adding item: " + itemID);
                        inventory.add_item(itemID);
                        events.displayChoices("You defeated the " + enemy.name + " which dropped a(n) " + r2.getString(2) + ".", "Continue");
                    }
                    else if (num_items == 0)
                        events.displayChoices("You defeated the " + enemy.name + ".", "Continue");
                    else{
                        ResultSet r2;
                        String q2 = "select item_id, item_name from ITEMS, DROPS where item_id" + 1 + "=item_id and " + "enemy_id=" + enemy_id;
                        r2 = db.executeQuery(q2);
                        int itemID = r2.getInt(1);
                        System.out.println("Adding item: " + itemID);
                        inventory.add_item(itemID);
                        events.displayChoices("You defeated the " + enemy.name + " which dropped a(n) " + r2.getString(2) + ".", "Continue");
                    }
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return true;
    }

    public int calculate_player_damage(Enemy enemy, Player player)
    {
        int end_damage = 0;
        int player_damage = 0;
        Random rand = new Random();
        int rand_damage = rand.nextInt(3);
        int rand_damage2 = rand.nextInt(5);
        int rand_chance = rand.nextInt(10);
        if(rand_chance < 3)
        {
            end_damage = (player.STRENGTH + rand_damage) + rand_damage2;
            if(end_damage <= 0)
            {
                end_damage = 0;
            }
        }
        else
        {
            end_damage = (player.STRENGTH + rand_damage);
            if(end_damage <= 0)
            {
                end_damage = 0;
            }
        }
        return end_damage;
    }

    public int calculate_enemy_damage(Enemy enemy, Player player)
    {
        int end_damage = 0;
        Random rand = new Random();
        int rand_damage = rand.nextInt(3);
        int rand_damage2 = rand.nextInt(4);
        int rand_chance = rand.nextInt(10);
        if(rand_chance < 2)
        {
            end_damage = (enemy.damage + rand_damage) - player.DEFENSE - rand_damage2;
            if(end_damage <= 0)
            {
                end_damage = 0;
            }
        }
        else
        {
            end_damage = (enemy.damage + rand_damage) - player.DEFENSE;
            if(end_damage <= 0)
            {
                end_damage = 0;
            }
        }
        return end_damage;
    }
}
