//
//  LocationObserver.swift
//  CommunityBus
//
//  Created by KomoriSoto on 2020/10/07.
//  Copyright © 2020 EhimeUniversity. All rights reserved.
//

import Foundation
import CoreLocation
import Combine

class LocationObserver: NSObject, ObservableObject, CLLocationManagerDelegate {
  @Published private(set) var location = CLLocation()
  
  private let locationManager: CLLocationManager
  
  override init() {
    self.locationManager = CLLocationManager()
    
    super.init()
    
    self.locationManager.delegate = self
    self.locationManager.requestWhenInUseAuthorization()
    self.locationManager.startUpdatingLocation()
  }
  
  func locationManager(_: CLLocationManager, didUpdateLocations: [CLLocation]) {
    location = didUpdateLocations.last!
    
  }
  
}
