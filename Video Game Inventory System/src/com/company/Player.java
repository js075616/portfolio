/**
 * @file Player.java
 * @brief Holds player info
 * @author Jake Schwarz
 */
package com.company;

public class Player
{
    int HP;
    int STRENGTH;
    int DEFENSE;
    int currentMana, baseMana;


    Player()
    {
        HP = 30;
        STRENGTH = 1;
        DEFENSE = 1;
        baseMana = 30;
        currentMana = 30;

    }

    public void increase_defense(int increase)
    {
        if(increase == 99)
        {
            DEFENSE = 999;
        }
        else
            {
            DEFENSE += increase;
        }
    }

    public void decrease_defense(int decrease)
    {
        DEFENSE -= decrease;
    }

    public void increase_strength(int increase)
    {
        if(increase == 99)
        {
            STRENGTH = 999;
        }
        else
        {
            STRENGTH += increase;
        }
    }

    public void decrease_strength(int decrease)
    {
        STRENGTH -= decrease;
    }

    public void increase_hp(int increase)
    {
        if(increase == 99)
        {
            HP = 999;
        }
        else if(increase + HP > 30)
        {
            HP = 30;
        }
        else {
            HP += increase;
        }
    }

    public void decrease_hp(int decrease)
    {
        HP -= decrease;
    }

    void recoverMana( int mana )
    {
        currentMana += mana;

        if ( currentMana > baseMana )
        {
            currentMana = baseMana;
        }
    }
}
