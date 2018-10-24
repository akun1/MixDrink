//
//  ViewController.swift
//  MixDrink
//
//  Created by Krista Capps on 10/22/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
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
        performSegue(withIdentifier: "toLogin", sender: self)
    }

}

