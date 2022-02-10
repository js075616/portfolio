/**
 * @file Coins.java
 * @brief Contains methods necessary for a coin system.
 * @author Jake Schwarz
 */

package com.company;

public class Coins
{
    int balance = 10; //intializes coin balance to 10

    /**
     * @brief Shows the value of a Coins object. Currently unused.
     * @return
     */
    public int get_coins()
    {
        return balance;
    }

    /**
     * @brief Adds coins to the balance.
     * @param added_coins Number of coins to be added.
     */
    public void add_coins(int added_coins)
    {
        balance += added_coins;
    }

    /**
     * @brief Removes coins from the balance.
     * @param minus_coins Number of coins to be removed.
     */
    public void subtract_coins(int minus_coins)
    {
        balance -= minus_coins;
    }

    /**
     * @brief Shows the amount of coins available in the balance.
     */
    public void show_coins()
    {
        System.out.print("Coins: ");
        System.out.println(balance);
    }
}
