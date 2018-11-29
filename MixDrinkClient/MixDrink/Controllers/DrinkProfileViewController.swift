//
//  DrinkProfileViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 11/26/18.
//  Copyright © 2018 Akash Kundu. All rights reserved.
//

import UIKit

class DrinkProfileViewController: UIViewController {

    @IBOutlet weak var confidenceLabel: UILabel!
    @IBOutlet weak var drinkIngrs: UILabel!
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
        drinkIngrs.text = Me.shared.currentDrink.indgredients.getStringOfAllNames()
        confidenceLabel.text = "\(String(format: "%.2f", arguments: [100.0*Me.shared.currentDrink.confidence]))% Confident"
    }

    @IBAction func dissmissProfile(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
}
