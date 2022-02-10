package com.company;

import java.util.ArrayList;
import java.util.Random;

public class Spells {

    static final String[] spells = { "Fireball", "Cure", "Lightning Bolt", "Blinding Light", "Protect" };
    int lastUnlocked = 1;
    Player player;

    public Spells( Player player )
    {
        this.player = player;
    }

    // Returns true if spell was cast, false otherwise
    int displaySpells()
    {
        String[] tempArr = new String[lastUnlocked + 2];

        for ( int i = 0; i <= lastUnlocked && i < spells.length ; ++i )
        {
            tempArr[i] = spells[i];
        }

        tempArr[ tempArr.length - 1 ] = "Return";

        int result =  Events.inst.displayChoices("Choose a spell",  tempArr );

        if ( result < tempArr.length )
            return result;
        else
            return -1;
    }

    String castSpell( Enemy enemy, int index, boolean chance )
    {
        String spellToCast =  spells[--index];
        String effectText = "";

        //System.out.println("casting: " + spellToCast );

        if ( spellToCast.equals("Fireball") )
        {
            if ( player.currentMana < 3 )
            {
                effectText = "Insufficient Mana.";
            }
            else
            {
                player.currentMana -= 3;
                int enemy_damage = Combat.inst.calculate_enemy_damage( enemy, player );
                enemy.HP -= 5;

                if ( !chance )
                {
                    effectText = "You dealt 5 damage to the " + enemy.name + ". They dealt " + enemy_damage + " to you in retaliation.";
                    player.decrease_hp( enemy_damage );
                }
                else
                {
                    effectText = "You dealt 5 damage to the " + enemy.name + ". The " + enemy.name + " missed after being stumbled by your previous guard.";
                    chance = false;
                }
            }
        }
        else if ( spellToCast.equals("Cure") )
        {
            if ( player.currentMana < 10 )
            {
                effectText = "Insufficient Mana.";
            }
            else
            {
                player.currentMana -= 10;
                int enemy_damage = Combat.inst.calculate_enemy_damage( enemy, player );

                if ( !chance )
                {
                    effectText = "You restore 10 HP. The " + enemy.name + " dealt " + enemy_damage + " to you.";
                    player.increase_hp( 10 );
                    player.decrease_hp( enemy_damage );
                }
                else
                {
                    effectText = "You restore 10 HP. The " + enemy.name + " missed after being stumbled by your previous guard.";
                    player.increase_hp( 10 );
                    chance = false;
                }
            }
        }
        else if ( spellToCast.equals("Lightning Bolt") )
        {
            if ( player.currentMana < 5 )
            {
                effectText = "Insufficient Mana.";
            }
            else
            {
                player.currentMana -= 5;
                int enemy_damage = Combat.inst.calculate_enemy_damage( enemy, player );
                enemy.HP -= 10;

                if ( !chance )
                {
                    effectText = "You dealt 10 damage to the " + enemy.name + ". They dealt " + enemy_damage + " to you in retaliation.";
                    player.decrease_hp( enemy_damage );
                }
                else
                {
                    effectText = "You dealt 10 damage to the " + enemy.name + ". The " + enemy.name + " missed after being stumbled by your previous guard.";
                    chance = false;
                }
            }
        }
        else if ( spellToCast.equals("Blinding Light") )
        {
            if ( player.currentMana < 2 )
            {
                effectText = "Insufficient Mana.";
            }
            else
            {
                player.currentMana -= 2;
                int enemy_damage = Combat.inst.calculate_enemy_damage( enemy, player );
                enemy.HP -= 2;

                if ( !chance )
                {
                    Random rand = new Random();

                    if ( rand.nextInt(10) < 5 )
                    {
                        effectText = "You dealt 2 damage to the " + enemy.name + ". They dealt " + enemy_damage + " to you in retaliation.";
                        player.decrease_hp( enemy_damage );
                    }
                    else
                    {
                        effectText = "You dealt 2 damage to the " + enemy.name + ". The flash of light causes the " + enemy.name + " to miss their attack.";
                    }
                }
                else
                {
                    effectText = "You dealt 2 damage to the " + enemy.name + ". The " + enemy.name + " missed after being stumbled by your previous guard.";
                    chance = false;
                }
            }
        }
        else if ( spellToCast.equals("Protect") )
        {
            if ( player.currentMana < 2 )
            {
                effectText = "Insufficient Mana.";
            }
            else
            {
                player.currentMana -= 2;
                effectText = "You protect and take no damage.";
            }
        }

        return effectText;
    }
}
