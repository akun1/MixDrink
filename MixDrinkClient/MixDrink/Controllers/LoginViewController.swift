//
//  LoginViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/23/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    func goToHome() {
        //load user data here
        loadUserData()
        
        //when done, perform segue here
        performSegue(withIdentifier: "toHome", sender: self)
    }
    
    func goToQuiz() {
        performSegue(withIdentifier: "toQuiz", sender: self)
    }
    
    func loadUserData() {
        print("loading user data...")
    }
    
    func login() {
        print("logging in...")
        goToHome()
    }
    
    @IBAction func loginTapped(_ sender: Any) {
        login()
    }
    
}
