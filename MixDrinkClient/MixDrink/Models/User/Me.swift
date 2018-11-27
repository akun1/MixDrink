//
//  Me.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/23/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class Me : NSObject {
    
    static var shared = Me()
    var myDrinks : Drinks = Drinks()
    var myLikedDrinks : Drinks = Drinks()
    var myIngrs : Ingredients = Ingredients()
    var myLikedIngrs : Ingredients = Ingredients()
    var currentDrink : Drink = Drink()
    
    private override init() {}
    
    

}
