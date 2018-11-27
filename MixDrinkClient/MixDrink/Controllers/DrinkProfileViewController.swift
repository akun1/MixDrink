//
//  DrinkProfileViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/26/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class DrinkProfileViewController: UIViewController {

    @IBOutlet weak var drinkName: UILabel!
    @IBOutlet weak var drinkImage: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        setup()
    }
    
    func setup() {
        drinkName.text = Me.shared.currentDrink.name
        drinkImage.downloaded(from: Me.shared.currentDrink.imageURL)
    }

    @IBAction func dissmissProfile(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
}
