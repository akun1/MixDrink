//
//  ViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/22/18.
//  Copyright © 2018 Akash Kundu. All rights reserved.
//

import UIKit

class LauncherViewController: UIViewController {

   override func viewDidLoad() {
      super.viewDidLoad()
   }
    
    override func viewDidAppear(_ animated: Bool) {
        goToLogin()
    }

    
    func goToLogin() {
        performSegue(withIdentifier: "toHome", sender: self)
    }

}

