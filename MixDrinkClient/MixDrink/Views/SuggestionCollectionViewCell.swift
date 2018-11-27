//
//  SuggestionCollectionViewCell.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/16/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class SuggestionCollectionViewCell: UICollectionViewCell {
    
    @IBOutlet weak var image: UIImageView!
    @IBOutlet weak var percentMatch: UILabel!
    @IBOutlet weak var name: UILabel!
    var suggestionDrink : Drink?
    
//    override func awakeFromNib() {
//        super.awakeFromNib()
//        // Initialization code
//    }

    
    @IBAction func likeTapped(_ sender: Any) {
        if let drink = suggestionDrink {
            let drinkNames = Me.shared.myLikedDrinks.drinks.map({$0.name})
            if !drinkNames.contains(drink.name) {
                Me.shared.myLikedDrinks.drinks.append(drink)
            }
        }
        let generator = UIImpactFeedbackGenerator(style: .heavy)
        generator.impactOccurred()
        
        pushFavoriteDrinks()
    }
    
    @IBAction func dislikeTapped(_ sender: Any) {
        if let drink = suggestionDrink {
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
        }
    }
    
}
