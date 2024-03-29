//
//  SuggestedDrinksViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/31/18.
//  Copyright © 2018 Akash Kundu. All rights reserved.
//

import UIKit
import UserNotifications

private let reuseIdentifier = "drink"

class SuggestedDrinksViewController: UIViewController, UICollectionViewDelegate, UICollectionViewDataSource {
    
    @IBOutlet weak var welcomeLabel: UILabel!
    @IBOutlet weak var collectionView: UICollectionView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        NotificationCenter.default.addObserver(self, selector: #selector(updateRecs(_:)), name: Notification.Name(rawValue: "RecsUpdated"), object: nil)
        
        welcomeLabel.text = "Woo, it's \(getTime())! Time to drink. 🙏 Here are some drinks we think you'd love!"
        
        setupCollectionView()
        pullSuggestions()
        
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false
        
        // Do any additional setup after loading the view.
    }
    
    @objc func updateRecs(_ notification: Notification) {
        DispatchQueue.main.async {
            self.collectionView.reloadData()
        }
    }
    
    func getTime() -> String {
        let date = Date()
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        let minutes = calendar.component(.minute, from: date)
        
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm a"
        return formatter.string(from: Date())
        
        //return "\(hour):\(minutes)"
    }
    
    func pullSuggestions() {
        API.loadDrinks {
            print("finished loading")
            DispatchQueue.main.sync {
                self.collectionView.reloadData()
            }
        }
    }
    
    // MARK: UICollectionViewDataSource
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }
    
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of items
        return Me.shared.myDrinks.count()
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        guard let cell = collectionView.dequeueReusableCell(withReuseIdentifier: reuseIdentifier, for: indexPath) as? SuggestionCollectionViewCell else { return UICollectionViewCell() }
        
        // Configure the cell
        cell.layer.applySketchShadow()
        cell.layer.applyRoundedCorners()
        
        let drink = Me.shared.myDrinks.drinks[indexPath.row]
        
        cell.suggestionDrink = drink
        cell.name.text = drink.name
        cell.image.downloaded(from: drink.imageURL)
        cell.percentMatch.text = "\(String(format: "%.2f", arguments: [100.0*drink.confidence]))% Confident"
        return cell
    }
    
    func collectionView(collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAtIndexPath indexPath: NSIndexPath) -> CGSize {
        let screenWidth = view.frame.width
        return CGSize(width: screenWidth/3, height: screenWidth/3);
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        guard let cell = collectionView.cellForItem(at: indexPath) as? SuggestionCollectionViewCell else { return }
        if let drink = cell.suggestionDrink {
            Me.shared.currentDrink = drink
        } else {
            Me.shared.currentDrink = Drink()
        }
        performSegue(withIdentifier: "toDrinkProfileFromSuggestion", sender: self)
    }
    
    
    func setupCollectionView() {
        let screenWidth = view.frame.width
        let layout: UICollectionViewFlowLayout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: 20, left: 5, bottom: 10, right: 5)
        layout.itemSize = CGSize(width: screenWidth/2 - 10, height: screenWidth/2)
        layout.minimumInteritemSpacing = 0
        layout.minimumLineSpacing = 10
        collectionView!.collectionViewLayout = layout
    }
    
    @IBAction func refreshSuggestions(_ sender: Any) {
        API.loadDrinks {
            DispatchQueue.main.async {
                self.collectionView.reloadData()
            }
        }
    }
    // MARK: UICollectionViewDelegate
    
    /*
     // Uncomment this method to specify if the specified item should be highlighted during tracking
     override func collectionView(_ collectionView: UICollectionView, shouldHighlightItemAt indexPath: IndexPath) -> Bool {
     return true
     }
     */
    
    /*
     // Uncomment this method to specify if the specified item should be selected
     override func collectionView(_ collectionView: UICollectionView, shouldSelectItemAt indexPath: IndexPath) -> Bool {
     return true
     }
     */
    
    /*
     // Uncomment these methods to specify if an action menu should be displayed for the specified item, and react to actions performed on the item
     override func collectionView(_ collectionView: UICollectionView, shouldShowMenuForItemAt indexPath: IndexPath) -> Bool {
     return false
     }
     
     override func collectionView(_ collectionView: UICollectionView, canPerformAction action: Selector, forItemAt indexPath: IndexPath, withSender sender: Any?) -> Bool {
     return false
     }
     
     override func collectionView(_ collectionView: UICollectionView, performAction action: Selector, forItemAt indexPath: IndexPath, withSender sender: Any?) {
     
     }
     */
}

