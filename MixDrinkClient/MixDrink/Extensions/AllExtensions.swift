//
//  AllExtensions.swift
//  MixDrink
//
//  Created by Akash Kundu on 10/31/18.
//  Copyright © 2018 Krista Capps. All rights reserved.
//

import Foundation
import UIKit

extension CALayer {
    
    func applySketchShadow(
        color: UIColor = UIColor.black,
        alpha: Float = 0.4,
        x: CGFloat = 0,
        y: CGFloat = 2,
        blur: CGFloat = 4,
        spread: CGFloat = 0)
    {
        shadowColor = color.cgColor
        shadowOpacity = alpha
        shadowOffset = CGSize(width: x, height: y)
        shadowRadius = blur / 2.0
        if spread == 0 {
            shadowPath = nil
        } else {
            let dx = -spread
            let rect = bounds.insetBy(dx: dx, dy: dx)
            shadowPath = UIBezierPath(rect: rect).cgPath
        }
    }
    
    func applyRoundedCorners(masks: Bool = false) {
        cornerRadius = 4
        borderWidth = 1.0
        borderColor = UIColor.clear.cgColor
        masksToBounds = masks
    }
}

