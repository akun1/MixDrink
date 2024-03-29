//
//  QuizTableViewCell.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/31/18.
//  Copyright © 2018 Akash Kundu. All rights reserved.
//

import UIKit

class QuizTableViewCell: UITableViewCell {

    @IBOutlet weak var quizCardView: UIView!
    @IBOutlet weak var yesButton: UIButton!
    @IBOutlet weak var noButton: UIButton!
    @IBOutlet weak var questionLabel: UILabel!
    var questionIngr : Ingredient?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        
        stylize()
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    func stylize() {
        questionLabel.lineBreakMode = .byWordWrapping
        self.selectionStyle = .none
        quizCardView.layer.applyRoundedCorners()
        quizCardView.layer.applySketchShadow()
        questionLabel.textColor = Theme.getThemeColorTeal()
        quizCardView.backgroundColor = UIColor.white
    }
    
    @IBAction func likeTapped(_ sender: Any) {
        let generator = UIImpactFeedbackGenerator(style: .heavy)
        generator.impactOccurred()
    }
    @IBAction func dislikeTapped(_ sender: Any) {
        let generator = UIImpactFeedbackGenerator(style: .heavy)
        generator.impactOccurred()
    }
    
    
}
