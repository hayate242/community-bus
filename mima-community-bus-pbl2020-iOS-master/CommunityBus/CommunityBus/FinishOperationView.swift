//
//  OperationInitialSettingView.swift
//  CommunityBus
//
//  Created by KomoriSoto on 2020/09/07.
//  Copyright © 2020 EhimeUniversity. All rights reserved.
//

import SwiftUI
import RealmSwift

struct FinishOperationView: View {
    @ObservedObject var busdata = busData()
    @ObservedObject var drivedata = driveData()
    @Binding var isActiveOperationInitialSettingView: Bool
    @State var isActiveOperationInfoView = false
    @State var tripMeterEndWith = ""
    @State var selected = 0
    @State var showingFinishAlert = false
    @State var showingErrorAlert = false
    @State var showingInvalidInputAlert = false
    @State var cannotSendOperationInfoAlert = false
    @State var apiErrorAlert = false
    
    let fontSize = 20
    
    var body: some View {
        ZStack {
            Color.gray.opacity(0.1)
                .edgesIgnoringSafeArea(.all)
            VStack {
                NavigationLink(destination: OperationInfoView(isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView),
                               isActive: $isActiveOperationInfoView) {
                    EmptyView()
                }.isDetailLink(false)
                .navigationBarTitle("業務終了画面", displayMode: .inline)
                Form {
                    Section(header: Text("業務終了").font(.system(size: CGFloat(self.fontSize)))){
                        HStack{
                            Text("業務終了時のトリップメーター(km)")
                                .font(.system(size: CGFloat(self.fontSize)))
                            TextField("ここにトリップメーターの値を入力", text: $tripMeterEndWith)
                                .multilineTextAlignment(.trailing)
                                .font(.system(size: CGFloat(self.fontSize)))
                                .keyboardType(.numberPad)
                        }
                        ZStack{
                            Button(action: {
                                if(self.tripMeterEndWith == ""){
                                    self.showingErrorAlert = true
                                }
                                else if(Int(tripMeterStartWith)! > Int(self.tripMeterEndWith)!){
                                    self.showingInvalidInputAlert = true
                                }
                                else{
                                    self.showingFinishAlert = true
                                }
                            })
                            {
                                Text("本日の業務終了")
                                    .font(.system(size: CGFloat(self.fontSize)))
                            }
                            .alert(isPresented: $showingFinishAlert){
                                Alert(
                                    title: Text("本日の業務を終了してもよろしいですか？"),
                                    primaryButton: .destructive(Text("いいえ")),
                                    secondaryButton: .default(Text("はい"),
                                                              action: {
                                                                //                          現時刻を取得
                                                                let date = Date()
                                                                
                                                                let format = DateFormatter()
                                                                format.dateFormat = "yyyy-MM-dd HH:mm:ss"
                                                                format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
                                                                
                                                                let callAPI = CallAPI.init()
                                                                // 送信用の業務終了情報
                                                                let finishServiceDict: [String: Any] = [
                                                                    "bus_id": bus_id,
                                                                    "driver_id": driver_id,
                                                                    "course_id": course_id,
                                                                    "trip_meter": self.tripMeterEndWith,
                                                                    "money": moneyAmount,
                                                                    "work_start_end_flag": "1",
                                                                    "send_at": String(format.string(from: date))
                                                                ]
                                                                
                                                                do{
                                                                    if monitor.currentPath.status == .unsatisfied{
                                                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                                                    }
                                                                    //業務情報の送信
                                                                    let jsonDataInit = callAPI.requestData(url: "/bus/init/create/", dict: finishServiceDict, type: "POST")
                                                                    if apiErrorFlag == true{
                                                                        apiErrorAlert = true
                                                                        apiErrorFlag = false
                                                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                                                    }
                                                                    _ = try JSONDecoder().decode(Success.self, from: jsonDataInit)
                                                                    
                                                                    //                                                        DBを削除
                                                                    let realm = try! Realm()
                                                                    try! realm.write {
                                                                        realm.deleteAll()
                                                                    }
                                                                    
                                                                    //                                                        トークンの破棄
                                                                    UserDefaults.standard.removeObject(forKey: "token")
                                                                    
                                                                    //入力値の変更
                                                                    busdata.havingmoney = moneyAmount
                                                                    busdata.tripMeter = self.tripMeterEndWith
                                                                    
                                                                    //入力値の破棄
                                                                    drivedata.addAmount = 0
                                                                    drivedata.customoerAmount = 0
                                                                    
 
                                                                    self.isActiveOperationInitialSettingView = false
                                                                }catch{
                                                                    if self.apiErrorAlert == false {
                                                                    self.cannotSendOperationInfoAlert = true
                                                                    }
                                                                }
                                                              })
                                )
                            }
                            Text("")     // ダミーのView
                                .alert(isPresented: $showingErrorAlert){
                                    Alert(title: Text("警告"),
                                          message: Text("トリップメーターの値が入力されていません。"),
                                          dismissButton: .default(Text("ok")))
                                }
                            Text("")     // ダミーのView
                                .alert(isPresented: $showingInvalidInputAlert){
                                    Alert(
                                        title: Text("エラー"),
                                        message: Text("業務開始時のトリップメーターの値よりも小さい値が入力されています。このまま登録してもよろしいですか？"),
                                        primaryButton: .destructive(Text("いいえ")),
                                        secondaryButton: .default(Text("はい"),
                                                                  action: {
                                                                    //                          現時刻を取得
                                                                    let date = Date()
                                                                    
                                                                    let format = DateFormatter()
                                                                    format.dateFormat = "yyyy-MM-dd HH:mm:ss"
                                                                    format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
                                                                    let callAPI = CallAPI.init()
                                                                    // 送信用の業務情報
                                                                    let finishServiceDict: [String: Any] = [
                                                                        "bus_id": bus_id,
                                                                        "driver_id": driver_id,
                                                                        "course_id": course_id,
                                                                        "trip_meter": self.tripMeterEndWith,
                                                                        "money": moneyAmount,
                                                                        "work_start_end_flag": "1",
                                                                        "send_at": String(format.string(from: date))
                                                                    ]
                                                                    
                                                                    do{
                                                                        if monitor.currentPath.status == .unsatisfied{
                                                                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                                                        }
                                                                        //業務情報の送信
                                                                        let jsonDataInit = callAPI.requestData(url: "/bus/init/create/", dict: finishServiceDict, type: "POST")
                                                                        _ = try JSONDecoder().decode(Success.self, from: jsonDataInit)
                                                                        
                                                                        //                                                        トークンの破棄
                                                                        UserDefaults.standard.removeObject(forKey: "token")

                                                                    
                                                                        //入力値の破棄
                                                                         busdata.havingmoney = ""
                                                                        busdata.tripMeter = ""
                                                                        drivedata.addAmount = 0
                                                                        drivedata.customoerAmount = 0
                                                              
                                                                        
                                                                        self.isActiveOperationInitialSettingView = false
                                                                    }catch{
                                                                        self.cannotSendOperationInfoAlert = true
                                                                    }
                                                                  })
                                    )
                                }
                        }
                    }
                }.alert(isPresented: self.$cannotSendOperationInfoAlert){
                    Alert(title: Text("通信エラー"),
                          message: Text("業務情報の登録に失敗しました")
                    )
                }
                Text("")
                .alert(isPresented: $apiErrorAlert){
                    Alert(
                        title: Text("送信に失敗しました"),
                        message: Text("もう一度お試しください")
                    )
                }
            }.frame(maxWidth: UIScreen.main.bounds.width * 4 / 5)
        }
    }
}
