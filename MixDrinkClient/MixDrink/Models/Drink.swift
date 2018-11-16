//
//  Drink.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/16/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class Drink: NSObject {
    
    var imageURL : String = ""
    var name : String = ""
    var indgredients : [String] = []
    var rating : String = ""
    var percentMatch : String = ""
    
    override init() {
        super.init()
    }
}

class Drinks: NSObject {
    
    var drinks : [Drink] = []
    
    override init() {
        super.init()
    }
    
    func count() -> Int {
        return drinks.count
    }
}
