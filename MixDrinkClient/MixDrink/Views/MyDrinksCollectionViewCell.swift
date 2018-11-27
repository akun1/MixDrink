//
//  MyDrinksCollectionViewCell.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/19/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit
import UserNotifications
class MyDrinksCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var drinkImage: UIImageView!
    @IBOutlet weak var drinkName: UILabel!
    var drink : Drink?
    
    @IBAction func dislikeTapped(_ sender: Any) {
        if let drink = drink {
            let filteredDrinks : Drinks = Drinks()
            filteredDrinks.drinks = Me.shared.myLikedDrinks.drinks.filter({$0.name != drink.name})
            Me.shared.myLikedDrinks = filteredDrinks
        }
        let generator = UIImpactFeedbackGenerator(style: .heavy)
        generator.impactOccurred()
        
        pushFavoriteDrinks()
    }
    
    func pushFavoriteDrinks() {
        print("Sending post now!")
        API.sendFavoriteDrinks {
            print("Sending of favs complete")
            NotificationCenter.default.post(name: Notification.Name(rawValue: "RecsUpdated"), object: nil)
            NotificationCenter.default.post(name: Notification.Name(rawValue: "FavsUpdated"), object: nil)
        }
    }
}
