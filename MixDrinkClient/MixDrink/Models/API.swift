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
        
        var newDrinks : [Drink] = []
        
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
                        if let imageUrl = d["strDrinkThumb"] as? String {
                            drink.imageURL = imageUrl
                        }
                        if let rating = d["rating"] as? String {
                            drink.rating = rating
                        }
                        if let confidence = d["confidence"] as? Double {
                            drink.confidence = confidence
                        }
                        if let name = d["strDrink"] as? String {
                            drink.name = name
                        }
                        if let ingrs = d["allIngredients"] as? [String] {
                            for i in ingrs {
                                let ingr = Ingredient(name: i)
                                drink.indgredients.all.append(ingr)
                                Me.shared.myIngrs.all.append(ingr)
                            }
                        }
                        
                        newDrinks.append(drink)
                    
//                        if Me.shared.myDrinks.containsDrinkWithName(drinkName: drink.name) {
//                            Me.shared.myDrinks.setConfidenceOfDrinkWithName(drinkName: drink.name, confidence: drink.confidence)
//                        } else {
//                            Me.shared.myDrinks.drinks.append(drink)
//                        }
                        
                    }
                    
                    print(newDrinks.map({$0.name}))
                    
                    //each load should only have DUPES and NEW ones.
                    //print(Me.shared.myDrinks.drinks.map({$0.name}))
                    Me.shared.myDrinks.drinks = Array(newDrinks.sorted(by: { (d1, d2) -> Bool in
                        d1.confidence > d2.confidence
                    }).prefix(10))
                    
                    //print(Me.shared.myDrinks.drinks.map({$0.name}))
                    finished()
                }
            } catch {
                print("error with json resp")
                finished()
            }
            }.resume()
    }
    
    static func sendFavoriteDrinks(finished: @escaping () -> Void) {
        
//        print("\n---------------")
//        print(Me.shared.myLikedDrinks.getListOfNames())
//        print("------------------\n")
        
        guard let url = URL(string: "http://35.165.13.8/recommendation") else {
            finished()
            return
        }
        
        //creating a POST request, sends parameters
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let postData = NSData(data: Me.shared.myLikedDrinks.getListOfNames().data(using: .utf8)!)
        
        //request.httpBody = Data(base64Encoded: Me.shared.myLikedDrinks.getListOfNames())
        //request.httpBody = Me.shared.myLikedDrinks.getListOfNames().data(using: .utf8)
        request.httpBody = postData as? Data
        print(Me.shared.myLikedDrinks.getListOfNames())
//        print("\n----------http body:----------\n")
//        print(request.httpBody)
        
        let headers = [
            "Content-Type": "text/plain"
        ]
        request.allHTTPHeaderFields = headers
        
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            
            if let error = error {
                print(error.localizedDescription)
                finished()
            }
            
            var newDrinks : [Drink] = []
            
            // parsing data
            do {
                if let data = data, let json = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                    for d in json {
                        let drink = Drink()
                        if let imageUrl = d["strDrinkThumb"] as? String {
                            drink.imageURL = imageUrl
                        }
                        if let rating = d["rating"] as? String {
                            drink.rating = rating
                        }
                        if let confidence = d["confidence"] as? Double {
                            drink.confidence = confidence
                        }
                        if let name = d["strDrink"] as? String {
                            drink.name = name
                        }
                        if let ingrs = d["allIngredients"] as? [String] {
                            for i in ingrs {
                                let ingr = Ingredient(name: i)
                                drink.indgredients.all.append(ingr)
                                Me.shared.myIngrs.all.append(ingr)
                            }
                        }
                        
                        newDrinks.append(drink)
                        
                        //                        if Me.shared.myDrinks.containsDrinkWithName(drinkName: drink.name) {
                        //                            Me.shared.myDrinks.setConfidenceOfDrinkWithName(drinkName: drink.name, confidence: drink.confidence)
                        //                        } else {
                        //                            Me.shared.myDrinks.drinks.append(drink)
                        //                        }
                        
                    }
                    
                    print(newDrinks.map({$0.name}))
                    
                    //each load should only have DUPES and NEW ones.
                    //print(Me.shared.myDrinks.drinks.map({$0.name}))
                    Me.shared.myDrinks.drinks = Array(newDrinks.sorted(by: { (d1, d2) -> Bool in
                        d1.confidence > d2.confidence
                    }).prefix(10))
                    
                    //print(Me.shared.myDrinks.drinks.map({$0.name}))
                    finished()
                }
            } catch {
                print("error with json resp")
                finished()
            }
            
//            // getting data and converting to string
//            if let data = data {
//                if let response = String(data: data, encoding: .utf8) {
//                    //print(response)
//                    finished()
//                }
//            }
            
            
            
            }.resume()
    }
    
}

