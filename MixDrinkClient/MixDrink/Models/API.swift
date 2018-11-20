//
//  Drink.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/16/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class API {
    
    static func loadDrinks(finished: @escaping () -> Void) {
        
        //url
        guard let url = URL(string: "http://35.165.13.8/recommendation") else { return }
        
        //creating request
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        //send request
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            
            // parsing data
            do {
                if let data = data, let json = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                    for d in json {
                        let drink = Drink()
                        print(d)
                        if let imageUrl = d["strDrinkThumb"] as? String {
                            drink.imageURL = imageUrl
                        }
                        if let rating = d["rating"] as? String {
                            drink.rating = rating
                        }
                        if let confidence = d["confidence"] as? Float {
                            drink.confidence = confidence
                        }
                        if let name = d["strDrink"] as? String {
                            drink.name = name
                        }
                        if let ingrs = d["allIngredients"] as? [String] {
                            for i in ingrs {
                                let ingr = Ingredient(name: i)
                                drink.indgredients.all.append(ingr)
                            }
                        }
                        
                        Me.shared.myDrinks.drinks.append(drink)
                    }
                    finished()
                }
            } catch {
                print("error with json resp")
                finished()
            }
            }.resume()
    }
    
    static func loadAllIngredients(finished: @escaping () -> Void) {
        
        //url
        guard let url = URL(string: "http://54.186.197.36/ingredients") else { return }
        
        //creating request
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        //send request
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            
            // parsing data
            do {
                if let data = data, let json = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                    for d in json {
                        let drink = Drink()
                        print(d)
                        if let imageUrl = d["strDrinkThumb"] as? String {
                            drink.imageURL = imageUrl
                        }
                        if let rating = d["rating"] as? String {
                            drink.rating = rating
                        }
                        if let confidence = d["confidence"] as? Float {
                            drink.confidence = confidence
                        }
                        if let name = d["strDrink"] as? String {
                            drink.name = name
                        }
                        
                        
                        Me.shared.myDrinks.drinks.append(drink)
                    }
                    finished()
                }
            } catch {
                print("error with json resp")
                finished()
            }
            }.resume()
    }
    
}
