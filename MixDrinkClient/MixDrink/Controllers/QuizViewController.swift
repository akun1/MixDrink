//
//  QuizViewController.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/31/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import UIKit

class QuizViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setupTableView()

        // Do any additional setup after loading the view.
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 4
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "question", for: indexPath) as? QuizTableViewCell else { return UITableViewCell() }
        
        cell.questionLabel.text = "Do you love alcahol?"
        
        return cell
    }
    
    func setupTableView() {
        let cell = UINib(nibName: "QuizTableViewCell", bundle: nil)
        tableView.register(cell, forCellReuseIdentifier: "question")
        tableView.estimatedRowHeight = 44
        tableView.rowHeight = UITableView.automaticDimension
        tableView.separatorStyle = .none
        tableView.allowsSelection = true
        tableView.backgroundColor = UIColor.clear
    }
}
