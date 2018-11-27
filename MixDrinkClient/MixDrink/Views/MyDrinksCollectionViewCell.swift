//
//  MyDrinksCollectionViewCell.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/19/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class MyDrinksCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var drinkImage: UIImageView!
    @IBOutlet weak var drinkName: UILabel!
    var drink : Drink?
}
