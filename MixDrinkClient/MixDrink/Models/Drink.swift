//
//  Drink.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/16/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

struct Ingredient {
    var name : String = ""
    init(name: String) {
        self.name = name
    }
}

struct Ingredients {
    var all : [Ingredient] = []
    var isLiked : Bool = true
    init() {}
}

class Drink: NSObject {
    
    var imageURL : String = ""
    var name : String = ""
    var indgredients : Ingredients = Ingredients()
    var rating : String = ""
    var confidence : Float = 0.0
    
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
