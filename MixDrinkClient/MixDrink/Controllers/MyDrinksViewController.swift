//
//  MyDrinksCollectionViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/31/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

private let reuseIdentifier = "drink"

class MyDrinksViewController: UIViewController, UICollectionViewDelegate, UICollectionViewDataSource {
    
    @IBOutlet weak var collectionView: UICollectionView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        NotificationCenter.default.addObserver(self, selector: #selector(updateFavs(_:)), name: Notification.Name(rawValue: "FavsUpdated"), object: nil)
        
        setupCollectionView()

        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Do any additional setup after loading the view.
    }
    
    @objc func updateFavs(_ notification: Notification) {
        DispatchQueue.main.async {
            self.collectionView.reloadData()
        }
    }

    func numberOfSections(in collectionView: UICollectionView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }


    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of items
        return Me.shared.myLikedDrinks.drinks.count
    }

    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        guard let cell = collectionView.dequeueReusableCell(withReuseIdentifier: reuseIdentifier, for: indexPath) as? MyDrinksCollectionViewCell else { return UICollectionViewCell() }
    
        let drink = Me.shared.myLikedDrinks.drinks[indexPath.row]
        // Configure the cell
        cell.layer.applySketchShadow()
        cell.layer.applyRoundedCorners()
    
        cell.drinkName.text = drink.name
        cell.drinkImage.downloaded(from: drink.imageURL)
        
        cell.drink = drink
        
        return cell
    }
    
    func collectionView(collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAtIndexPath indexPath: NSIndexPath) -> CGSize {
        let screenWidth = view.frame.width
        return CGSize(width: screenWidth/3, height: screenWidth/3);
    }
    
    
    func setupCollectionView() {
        let screenWidth = view.frame.width
        let layout: UICollectionViewFlowLayout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: 20, left: 5, bottom: 10, right: 5)
        layout.itemSize = CGSize(width: screenWidth/3 - 10, height: screenWidth/3)
        layout.minimumInteritemSpacing = 0
        layout.minimumLineSpacing = 10
        collectionView!.collectionViewLayout = layout
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        guard let cell = collectionView.cellForItem(at: indexPath) as? MyDrinksCollectionViewCell else { return }
        if let drink = cell.drink {
            Me.shared.currentDrink = drink
        } else {
            Me.shared.currentDrink = Drink()
        }
        performSegue(withIdentifier: "toDrinkProfileFromFav", sender: self)
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
