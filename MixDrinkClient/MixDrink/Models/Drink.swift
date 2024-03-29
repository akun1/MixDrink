//
//  Drink.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/16/18.
//  Copyright © 2018 Akash Kundu. All rights reserved.
//

import UIKit

struct Ingredient {
    var name : String = ""
    init(name: String) {
        self.name = name
    }
    
    func getName() -> String {
        return name
    }
}

struct Ingredients {
    var all : [Ingredient] = []
    var isLiked : Bool = true
    init() {}
    
    func getStringOfAllNames() -> String {
        return all.map({$0.getName()}).joined(separator: ", ")
    }
}

class Drink: NSObject {
    
    var imageURL : String = ""
    var name : String = ""
    var indgredients : Ingredients = Ingredients()
    var rating : String = ""
    var confidence : Double = 0.0
    
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
    
    func getListOfNames() -> String {
        let names = drinks.map({$0.name})
        var stringOfNames : String = names.joined(separator: ",")
        return "[" + stringOfNames + "]"
    }
    
    func containsDrinkWithName(drinkName: String) -> Bool {
        return drinks.map({$0.name}).contains(drinkName)
    }
    
    func setConfidenceOfDrinkWithName(drinkName: String, confidence: Double) {
        drinks.filter({$0.name == drinkName}).first?.confidence = confidence
    }
}
