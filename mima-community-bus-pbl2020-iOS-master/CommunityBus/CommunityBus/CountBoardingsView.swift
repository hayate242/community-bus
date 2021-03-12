//
//  CountBoardingsView.swift
//  CommunityBus
//
//  Created by KomoriSoto on 2020/09/07.
//  Copyright © 2020 EhimeUniversity. All rights reserved.
//

import SwiftUI
import CoreLocation
import RealmSwift

struct CountBoardingsView: View {
    @ObservedObject var drivedata = driveData()
    @Binding var isActiveOperationInitialSettingView: Bool
    @Binding var isActiveCountBoardingsView: Bool
    @Binding var route: String
    @Binding var routeOrder: String
    @State var isActiveOperationInfoView = false
    @State var autoSwitchBusStop = true
    @State var tripMeter = ""
    @State var showingSuccessfulAlert = false
    @State var showingErrorAlert = false
    @State var showingStartCountingAlert = false
    @State var showingFinishCountingAlert = false
    @State var showingMoneyAmountAlert = false
    @State var fontSize = 20
    @State var buttonOpacity = 0.4
    @State var buttonForegroundColor = Color.gray
    @State var buttonBackgroundColor = Color.gray
    @State var memo = ""
    @State var selectedBusStop = 0
    @State var autoSelectedBusStop = 0
    @State var maxBoardings = 9
    @State var boardingsArray = [[
        "getOff":[
            "numberGetOff": 0,
        ],
        "getOn":[
            "numberGetOnCash": 0,
            "numberGetOff": 0,
            "numberGetOnCashAdult": 0,
            "numberGetOnCashChild": 0,
            "numberGetOnCashHandicappedAdult": 0,
            "numberGetOnCashHandicappedChild": 0,
            "numberGetOnCouponAdult": 0,
            "numberGetOnCouponChild": 0,
            "numberGetOnCouponHandicapped": 0,
            "numberGetOnCommuterPass": 0,
            "numberGetOnFree": 0,
        ],
        "coupon":[
            "salesCouponAdult": 0,
            "salesCouponChild": 0,
            "salesCouponHandicapped": 0
        ]
    ]]
    @ObservedObject var locationObserver = LocationObserver()
    @State var busFare = BusFare()
    @State var lat:String = ""
    @State var lon:String = ""
    @State var startCountingButtonDisabled = false
    @State var finishOperationButtonDisabled = true
    @State var countButtonDisabled = true
    @State var busStopsListDisabled = false
    @State var buttonTitle = "入力開始"
    @State var autoSwitchingToggleDisabled = false
    @State var textFieldDisabled = true
    @State var showingCommunicatonError = false
    @State var boardingsInfoDict: [String: Array<Dictionary<String, String>>] = [:]
    @State var isFirstTime = true
    @State var totalBoardings = 0
    @State var soldCouponAmount = 0
    @State var cannotSendBoardingsError = false
    @Environment(\.presentationMode) var presentationMode: Binding<PresentationMode>
    @State var numberOfFareId = 13
    @State var next_stop: String = ""
    @State var apiErrorAlert = false
    @State var boardingsNumberArray:[Int] = []
    
    var body: some View {
        VStack(spacing: 10) {
            Form{
                HStack(){
                    Text(route)
                        .font(.system(size: CGFloat(self.fontSize)))
                        .frame(width: UIScreen.main.bounds.width / 4)
                        .minimumScaleFactor(0.0001)
                        .lineLimit(1)
                    Text(routeOrder)
                        .font(.system(size: CGFloat(self.fontSize)))
                        .frame(width: UIScreen.main.bounds.width / 4)
                        .minimumScaleFactor(0.0001)
                        .lineLimit(1)
                    Toggle(isOn: $autoSwitchBusStop){
                        Text("停留所の自動切替")
                            .font(.system(size: CGFloat(self.fontSize)))
                    }.disabled(autoSwitchingToggleDisabled)
                    .frame(width: UIScreen.main.bounds.width / 4)
                    .minimumScaleFactor(0.0001)
                    .lineLimit(1)
                    Picker(selection: $selectedBusStop,
                           label: Text(""))
                    {
                        //                            停留所一覧の表示
                        ForEach(0..<Int(busStops.count), id: \.self) {i in
                            Text(getBusStopName(busStops: busStops, index: i)+"\n乗車人数:"+String(boardingsNumberArray[i]))
                                .font(.system(size: CGFloat(self.fontSize)))
                        }
                    }.disabled(autoSwitchBusStop || busStopsListDisabled)
                    .onChange(of: self.selectedBusStop, perform: { value in
                        //                        便の最後の停留所になったら，運行終了ボタンの操作を有効にする
                        if selectedBusStop == Int(busStops.count)-1 && buttonTitle == "入力開始" {
                            finishOperationButtonDisabled = false
                        }
                        else{
                            finishOperationButtonDisabled = true
                        }
                        //                        メモの更新
                        for i in 0 ..< self.boardingsInfoDict["boardings"]!.count{
                            if(self.boardingsInfoDict["boardings"]![i]["memo"]! != "" && self.boardingsInfoDict["boardings"]![i]["bus_stop_order"]! == String(selectedBusStop+1)){
                                self.memo = self.boardingsInfoDict["boardings"]![i]["memo"]!
                                break
                            }else {
                                self.memo = ""
                            }
                        }
                    })
                }
            }
            
            HStack{
                Spacer()
                ZStack{
                    Button(action: {
                        if(self.buttonTitle == "入力開始"){
                            self.autoSwitchBusStop = false
                            self.showingStartCountingAlert = true
                        }
                        else if(self.buttonTitle == "入力終了"){
                            self.showingFinishCountingAlert = true
                        }
                    },
                    label: {
                        Text(self.buttonTitle)
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.medium)
                            .frame(minWidth: 160)
                            .foregroundColor(.white)
                            .padding(12)
                            .background(Color.accentColor)
                            .cornerRadius(8)
                    })
                    .alert(isPresented: $showingStartCountingAlert){
                        Alert.init(
                            title: Text("以下の停留所で乗降車数を\n記録しますか？"),
                            message: Text("現在の停留所：\(getBusStopName(busStops: busStops, index: selectedBusStop))"),
                            primaryButton:.destructive(Text("いいえ")),
                            secondaryButton: .default(Text("はい"),
                                                      action: {
                                                        self.buttonTitle = "入力終了"
                                                        self.autoSwitchingToggleDisabled = true
                                                        self.countButtonDisabled = false
                                                        self.buttonOpacity = 0.7
                                                        self.buttonForegroundColor = Color.black
                                                        self.buttonBackgroundColor = Color.gray
                                                        self.textFieldDisabled = false
                                                        self.busStopsListDisabled = true
                                                        finishOperationButtonDisabled = true
                                                      })
                        )
                    }
                    Text("")     // ダミーのView
                        .alert(isPresented: $showingFinishCountingAlert){
                            Alert.init(
                                title: Text("運行を再開します。\nよろしいですか？"),
                                primaryButton:.destructive(Text("いいえ")),
                                secondaryButton: .default(Text("はい"),
                                                          action: {
                                                            self.autoSwitchBusStop = true
                                                            self.countButtonDisabled = true
                                                            self.buttonTitle = "入力開始"
                                                            self.autoSwitchingToggleDisabled = false
                                                            self.buttonOpacity = 0.4
                                                            self.buttonForegroundColor = Color.gray
                                                            self.buttonBackgroundColor = Color.gray
                                                            self.textFieldDisabled = true
                                                            self.busStopsListDisabled = false
                                                            if selectedBusStop == busStops.count-1{
                                                                finishOperationButtonDisabled = false
                                                            }
                                                            
                                                            //                                                            メモ欄の登録
                                                            if(self.memo != ""){
                                                                for i in 0 ..< self.boardingsInfoDict["boardings"]!.count{
                                                                    if(self.boardingsInfoDict["boardings"]![i]["bus_stop_order"]! == String(self.selectedBusStop+1)){
                                                                        self.boardingsInfoDict["boardings"]![i].updateValue(self.memo, forKey: "memo")
                                                                    }
                                                                }
                                                            }
                                                            
                                                            //                                                            dbに保存
                                                            do{
                                                                let realm = try! Realm()
                                                                let bus_Stop_Id = String(self.selectedBusStop+1)
                                                                let date = Date()
                                                                let format = DateFormatter()
                                                                format.dateFormat = "yyyy-MM-dd"
                                                                format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
                                                                let time = String(format.string(from: date))
                                                                let updateData = realm.objects(boardings.self).filter("route_id == %@ AND route_order_id == %@ AND bus_stop_id == %@ AND date == %@", routeId, routeOrderId, bus_Stop_Id, time)
                                                                if(updateData.count != 0){
                                                                    for i in 0 ..< numberOfFareId{
                                                                        for j in 0 ..< self.boardingsInfoDict["boardings"]!.count{
                                                                            if(self.boardingsInfoDict["boardings"]![j]["bus_stop_order"]! == bus_Stop_Id && self.boardingsInfoDict["boardings"]![j]["fare_id"]! == String(i+1)){
                                                                                try realm.write(){
                                                                                    updateData[i].number = self.boardingsInfoDict["boardings"]![j]["number"]!
                                                                                    updateData[i].send_at = self.boardingsInfoDict["boardings"]![j]["send_at"]!
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }else{
                                                                    for i in 0 ..< numberOfFareId{
                                                                        for j in 0 ..< self.boardingsInfoDict["boardings"]!.count{
                                                                            if(self.boardingsInfoDict["boardings"]![j]["bus_stop_order"]! == bus_Stop_Id && self.boardingsInfoDict["boardings"]![j]["fare_id"]! == String(i+1)){
                                                                                let inputData = boardings()
                                                                                try realm.write(){
                                                                                    inputData.route_id = routeId
                                                                                    inputData.route_order_id = routeOrderId
                                                                                    inputData.bus_stop_id = bus_Stop_Id
                                                                                    inputData.fare_id = self.boardingsInfoDict["boardings"]![j]["fare_id"]!
                                                                                    inputData.number = self.boardingsInfoDict["boardings"]![j]["number"]!
                                                                                    inputData.send_at = self.boardingsInfoDict["boardings"]![j]["send_at"]!
                                                                                    inputData.date = time
                                                                                    realm.add(inputData)
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                            catch{
                                                            }
                                                          })
                            )
                        }
                }
                Spacer()
                Button(action: {
                    self.showingMoneyAmountAlert = true
                },
                label:{
                    Text("所持金額を確認")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.medium)
                        .frame(minWidth: 160)
                        .foregroundColor(.white)
                        .padding(12)
                        .background(Color.accentColor)
                        .cornerRadius(8)
                })
                .alert(isPresented: $showingMoneyAmountAlert){
                    Alert.init(
                        title: Text("所持金額は\(Int(moneyAmount)! +  self.drivedata.addAmount)円です"),
                        dismissButton: .default(Text("ok")))
                }
                Spacer()
            }
            
            HStack(spacing: 0){
                VStack() {
                    Text("降車数")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.orange.opacity(0.7))
                        .border(Color.black)
                    Text("")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.orange.opacity(0.7))
                        .border(Color.black)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOff", row2: "numberGetOff"))!
                        plusButtonpushed(row1: "getOff", row2: "numberGetOff", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOff", row2: "numberGetOff"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.orange.opacity(0.7))
                        .border(Color.black)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOff", row2: "numberGetOff"))!
                        minusButtonpushed(row1: "getOff", row2: "numberGetOff", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                }
                
                VStack(spacing: 0){
                    Text("乗車中：\(self.drivedata.customoerAmount)人")
                        .font(.system(size: CGFloat(35)))
                        .lineLimit(1)
                        .minimumScaleFactor(0.0001)
                        .frame(width: UIScreen.main.bounds.width * 15 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                    Text("現在：" +  String(getBusStopName(busStops: busStops, index: selectedBusStop)))
                        .font(.system(size: CGFloat(35)))
                        .minimumScaleFactor(0.0001)
                        .lineLimit(1)
                        .frame(width: UIScreen.main.bounds.width * 15 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                    Text("到着予定時刻：" + String((getArrivalTime(busStops: busStops, index: selectedBusStop))))
                        .font(.system(size: CGFloat(35)))
                        .minimumScaleFactor(0.0001)
                        .lineLimit(1)
                        .frame(width: UIScreen.main.bounds.width * 15 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                }
                
                VStack(spacing: 0){
                    Text("回数券の販売数")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 9 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.green.opacity(0.7))
                        .border(Color.black)
                    HStack(spacing: 0){
                        Text("大人")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                        Text("小人")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                        Text("障害者")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                    }
                    HStack(spacing: 0){
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponAdult"))!
                            plusButtonpushed(row1: "coupon", row2: "salesCouponAdult", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("＋")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponChild"))!
                            plusButtonpushed(row1: "coupon", row2: "salesCouponChild", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("＋")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponHandicapped"))!
                            plusButtonpushed(row1: "coupon", row2: "salesCouponHandicapped", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("＋")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                    }
                    HStack(spacing: 0){
                        Text(getBoardingsNumber(index: self.selectedBusStop, row1: "coupon", row2: "salesCouponAdult"))
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                        Text(getBoardingsNumber(index: self.selectedBusStop, row1: "coupon", row2: "salesCouponChild"))
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                        Text(getBoardingsNumber(index: self.selectedBusStop, row1: "coupon", row2: "salesCouponHandicapped"))
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(Color.green.opacity(0.7))
                            .border(Color.black)
                    }
                    HStack(spacing: 0){
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponAdult"))!
                            minusButtonpushed(row1: "coupon", row2: "salesCouponAdult", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("ー")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponChild"))!
                            minusButtonpushed(row1: "coupon", row2: "salesCouponChild", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("ー")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                        Button(action: {
                            let fareId = Int(getFareID(row1: "coupon", row2: "salesCouponHandicapped"))!
                            minusButtonpushed(row1: "coupon", row2: "salesCouponHandicapped", fare: getFare(fare_id: fareId))
                        },
                        label:{
                            Text("ー")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .fontWeight(.bold)
                                .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                                .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                                .foregroundColor(self.buttonForegroundColor)
                                .border(Color.black)
                        }).disabled(countButtonDisabled)
                    }
                }
            }
            
            VStack(spacing: 0){
                HStack(spacing: 0){
                    Text("乗車数")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 27 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                }
                HStack(spacing: 0){
                    Text("現金")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 12 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("回数券")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 9 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("定期券")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("無賃")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                }
                HStack(spacing: 0){
                    Text("大人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("小人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("障大人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text("障小人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text("大人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text("小人")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text("障害者")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text("")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text("")
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 2 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                }
                HStack(spacing:0){
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashAdult"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCashAdult", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashChild"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCashChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashHandicappedAdult"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCashHandicappedAdult", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashHandicappedChild"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCashHandicappedChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponAdult"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCouponAdult", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponChild"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCouponChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponHandicapped"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCouponHandicapped", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCommuterPass"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnCommuterPass", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnFree"))!
                        plusButtonpushed(row1: "getOn", row2: "numberGetOnFree", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("＋")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    
                }
                HStack(spacing: 0){
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCashAdult"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCashChild"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCashHandicappedAdult"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCashHandicappedChild"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCouponAdult"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCouponChild"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCouponHandicapped"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnCommuterPass"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                    Text(getBoardingsNumber(index: self.selectedBusStop, row1: "getOn", row2: "numberGetOnFree"))
                        .font(.system(size: CGFloat(self.fontSize)))
                        .fontWeight(.bold)
                        .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                        .background(Color.blue.opacity(0.7))
                        .border(Color.black)
                }
                HStack(spacing:0){
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashAdult"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCashAdult", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashChild"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCashChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashHandicappedAdult"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCashHandicappedAdult", fare: getFare(fare_id: fareId))
                        
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCashHandicappedChild"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCashHandicappedChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponAdult"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCouponAdult", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponChild"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCouponChild", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCouponHandicapped"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCouponHandicapped", fare: fareId)
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnCommuterPass"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnCommuterPass", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                    Button(action: {
                        let fareId = Int(getFareID(row1: "getOn", row2: "numberGetOnFree"))!
                        minusButtonpushed(row1: "getOn", row2: "numberGetOnFree", fare: getFare(fare_id: fareId))
                    },
                    label:{
                        Text("ー")
                            .font(.system(size: CGFloat(self.fontSize)))
                            .fontWeight(.bold)
                            .frame(width: UIScreen.main.bounds.width * 3 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                            .background(self.buttonBackgroundColor.opacity(self.buttonOpacity))
                            .foregroundColor(self.buttonForegroundColor)
                            .border(Color.black)
                    }).disabled(countButtonDisabled)
                }
            }
            TextField("ここにメモを記入", text: $memo)
                .font(.system(size: CGFloat(self.fontSize)))
                .border(Color.gray.opacity(0.7))
                .frame(width: UIScreen.main.bounds.width * 27 / 32, height: UIScreen.main.bounds.height * 1.5 / 32)
                .disabled(textFieldDisabled)
            
        }
        
        //コード上のイベントで遷移したい場合は、LabelにEmptyViewを指定する
        NavigationLink(destination: OperationInfoView( isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView),
                       isActive: $isActiveOperationInfoView) {
            EmptyView()
        }.isDetailLink(false)
        .navigationBarTitle("乗降者数入力画面", displayMode: .inline)
        .onAppear(){
            
            UIApplication.shared.isIdleTimerDisabled = true
            
            //                                    運賃の取得
            let callAPI = CallAPI.init()
            let jsonDataBusFare = callAPI.requestData(url: "/bus/fare/", dict: [:], type: "GET")
            self.busFare = try! JSONDecoder().decode(BusFare.self, from: jsonDataBusFare)
            
            // 5秒毎にバスのロケーションを送信，停留所の自動切替がonになっていたら，停留所の自動切替
            Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true, block: { (timer) in
                if isActiveCountBoardingsView {
                    lat = String(self.locationObserver.location.coordinate.latitude)
                    lon = String(self.locationObserver.location.coordinate.longitude)
                    if(self.autoSwitchBusStop == true){
                        sendBusLocation(longitude:lon,latitude:lat)
                        switchBusStop(longitude:lon, latitude: lat)
                    }
                }
                else{
                    timer.invalidate()
                }
            })
            
            //            停留所別かつ運賃区分別の乗降者数を保存するための配列
            for _ in 0 ..< (busStops.count-1){
                self.boardingsArray.append(self.boardingsArray[0])
            }
            
            //                          現時刻を取得
            let date = Date()
            let format = DateFormatter()
            format.dateFormat = "yyyy-MM-dd"
            format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
            let time = String(format.string(from: date))
            format.dateFormat = "yyyy-MM-dd HH:mm:ss"
            let realm = try! Realm()
            //        乗降情報一覧の作成
            if(self.boardingsInfoDict == [:]){
                for i in 0 ..< busStops.count{
                    boardingsNumberArray.append(0)
                    let busStopId:String = busStops[i]["bus_stop_id"]!
                    let filterData = realm.objects(boardings.self).filter("route_id == %@ AND route_order_id == %@ AND bus_stop_id == %@ AND date == %@", routeId, routeOrderId, busStopId, time)
                    for k in 0 ..< self.numberOfFareId{
                        var boardingsDict:[String: String] = [:]
                        if(filterData.count != 0){
                            boardingsDict = [
                                "bus_id": bus_id,
                                "route_id": routeId,
                                "route_order_id": routeOrderId,
                                "bus_stop_id": busStopId,
                                "bus_stop_order": String(i+1),
                                "driver_id": driver_id,
                                "fare_id": filterData[k].fare_id,
                                "number": filterData[k].number,
                                "memo": self.memo,
                                "send_at": filterData[k].send_at
                            ]
                            boardingsArray[i][getrow1(fare_id: k)]?[getrow2(fare_id: k)]! = Int(filterData[k].number) ?? 0
                            if getrow1(fare_id: k) == "getOn" {
                                boardingsNumberArray[i] += boardingsArray[i][getrow1(fare_id: k)]?[getrow2(fare_id: k)]! ?? 0
                            }
                        } else{
                            boardingsDict = [
                                "bus_id": bus_id,
                                "route_id": routeId,
                                "route_order_id": routeOrderId,
                                "bus_stop_id": busStopId,
                                "bus_stop_order": String(i+1),
                                "driver_id": driver_id,
                                "fare_id": String(k+1),
                                "number": "0",
                                "memo": self.memo,
                                "send_at": String(format.string(from: date))
                            ]
                        }
                        if(self.isFirstTime){
                            self.boardingsInfoDict = ["boardings": [boardingsDict]]
                            self.isFirstTime = false
                        }else{
                            self.boardingsInfoDict["boardings"]!.append(boardingsDict)
                        }
                    }
                }
            }
        }
        
        Button(action: {
            if(self.drivedata.customoerAmount == 0 || (self.drivedata.customoerAmount != 0 && self.memo != "")){
                self.showingSuccessfulAlert = true
            }
            else{
                self.showingErrorAlert = true
            }
        },
        label: {
            Text("運行終了")
                .font(.system(size: CGFloat(self.fontSize)))
                .fontWeight(.medium)
                .frame(minWidth: 160)
                .foregroundColor(.white)
                .padding(12)
                .background(Color.accentColor)
                .cornerRadius(8)
        }).disabled(finishOperationButtonDisabled)
        .alert(isPresented: $showingSuccessfulAlert){
            Alert.init(
                title: Text("以下の内容で運行を記録します\nよろしいですか？"),
                message: Text("累計乗車数：\(self.totalBoardings)人\n回数券の販売数：\(self.soldCouponAmount)枚\n所持金額：\(Int(moneyAmount)! + self.drivedata.addAmount)円"),
                primaryButton:.destructive(Text("いいえ")),
                secondaryButton: .default(Text("はい"),
                                          action: {
                                            
                                            //                        乗降情報の送信
                                            if(!self.boardingsInfoDict.isEmpty){
                                                DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                                                    do{
                                                        if monitor.currentPath.status == .unsatisfied{
                                                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                                        }
                                                        let callAPI = CallAPI.init()
                                                        let jsonDataBoardings = callAPI.requestData(url: "/bus/boardings/create/", dict: self.boardingsInfoDict, type: "POST")
                                                        if apiErrorFlag == true{
                                                            apiErrorAlert = true
                                                            apiErrorFlag = false
                                                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                                        }
                                                        _ = try JSONDecoder().decode(Success.self, from: jsonDataBoardings)
                                                        moneyAmount = String(Int(moneyAmount)! + self.drivedata.addAmount)
                                                        self.isActiveCountBoardingsView = false
                                                        selectedCourse += 1
                                                        if selectedCourse == numberOfCourseRoute{
                                                            selectedCourse = 0
                                                        }
                                                    }catch{
                                                        if self.apiErrorAlert == false {
                                                            self.cannotSendBoardingsError = true
                                                        }
                                                    }
                                                }
                                            }
                                          })
            )
        }
        Text("")     // ダミーのView
            .alert(isPresented: $showingErrorAlert){
                Alert(title: Text("警告"),
                      message: Text("乗車数と降車数が一致しません\n入力漏れ等ある場合、その旨をメモ欄に記入してください"),
                      dismissButton: .default(Text("ok")))
            }.navigationBarBackButtonHidden(true)
        Text("")     // ダミーのView
            .alert(isPresented: self.$cannotSendBoardingsError) {
                Alert(
                    title: Text("通信エラー"),
                    message: Text("乗降情報の登録に失敗しました")
                )
            }
        
        Text("")     // ダミーのView
            .alert(isPresented: self.$apiErrorAlert) {
                Alert(
                    title: Text("送信に失敗しました"),
                    message: Text("もう一度お試しください")
                )
            }
    }
    
    /// 乗降者数等のカウントアップと合計金額・現在の乗車数・回数券の販売数・累計乗車数を更新
    /// - Parameters:
    ///   - row1: 乗降種別（降車数，回数券の販売数，乗車数）
    ///   - row2: 乗降者種別（現金．回数券．定期，無賃＋大人，小人，障害者）
    ///   - fare: 選択された区分における料金
    func plusButtonpushed(row1:String,row2:String, fare:Int){
        if(!(self.drivedata.customoerAmount == 0 && row1 == "getOff")){
            boardingsArray[self.selectedBusStop][row1]?[row2]! += 1
            if(row1 == "getOff"){
                self.drivedata.customoerAmount -= 1
            }
            if(row1 == "getOn"){
                self.drivedata.customoerAmount += 1
                self.totalBoardings += 1
                boardingsNumberArray[self.selectedBusStop] += 1
            }
            if(row1 == "coupon"){
                self.soldCouponAmount += 1
            }
            self.drivedata.addAmount += fare
            let fareID = getFareID(row1:row1, row2:row2)
            updateBoardingsInfo(number: "1", fareID:fareID)
        }
    }
    
    /// 乗降者数等のカウントダウンと合計金額・現在の乗車数・回数券の販売数・累計乗車数を更新
    /// - Parameters:
    ///   - row1: 乗降種別（降車数，回数券の販売数，乗車数）
    ///   - row2: 乗降者種別（現金．回数券．定期，無賃＋大人，小人，障害者）
    ///   - fare: 選択された区分における料金
    func minusButtonpushed(row1:String,row2:String, fare:Int){
        if((boardingsArray[self.selectedBusStop][row1]?[row2]! != 0) && !(self.drivedata.customoerAmount == 0 && row1 == "getOn")){
            boardingsArray[self.selectedBusStop][row1]?[row2]! -= 1
            if(row1 == "getOff"){
                self.drivedata.customoerAmount += 1
            }
            if(row1 == "getOn"){
                self.drivedata.customoerAmount -= 1
                self.totalBoardings -= 1
                boardingsNumberArray[self.selectedBusStop] -= 1
            }
            if(row1 == "coupon"){
                self.soldCouponAmount -= 1
            }
            self.drivedata.addAmount -= fare
            let fareID = getFareID(row1:row1, row2:row2)
            updateBoardingsInfo(number: "-1", fareID: fareID)
        }
    }
    
    /// 運賃IDをリターンする
    /// - Parameters:
    ///   - row1: 乗降種別（降車数，回数券の販売数，乗車数）
    ///   - row2: 乗降者種別（現金．回数券．定期，無賃＋大人，小人，障害者）
    /// - Returns: 選択された区分における運賃ID
    func getFareID(row1:String, row2:String) -> String{
        switch row1 {
        case "getOff":
            return "1"
        case "getOn":
            switch row2 {
            case "numberGetOnCashAdult":
                return "2"
            case "numberGetOnCashChild":
                return "3"
            case "numberGetOnCashHandicappedAdult":
                return "4"
            case "numberGetOnCashHandicappedChild":
                return "5"
            case "numberGetOnCouponAdult":
                return"6"
            case "numberGetOnCouponChild":
                return "7"
            case "numberGetOnCouponHandicapped":
                return "8"
            case "numberGetOnCommuterPass":
                return "9"
            case "numberGetOnFree":
                return "10"
            default:
                return "0"
            }
        case "coupon":
            switch row2 {
            case "salesCouponAdult":
                return "11"
            case "salesCouponChild":
                return "12"
            case "salesCouponHandicapped":
                return "13"
            default:
                return "0"
            }
        default:
            return "0"
        }
    }
    func getrow1(fare_id: Int) -> String{
        if (fare_id == 0){
            return "getOff"
        }
        else if(fare_id == 10 || fare_id == 11 || fare_id == 12){
            return "coupon"
        }
        else{
            return "getOn"
        }
    }
    func getrow2(fare_id: Int) -> String{
        switch fare_id{
        case 0:
            return "numberGetOff"
        case 1:
            return "numberGetOnCashAdult"
        case 2:
            return "numberGetOnCashChild"
        case 3:
            return "numberGetOnCashHandicappedAdult"
        case 4:
            return "numberGetOnCashHandicappedChild"
        case 5:
            return "numberGetOnCouponAdult"
        case 6:
            return "numberGetOnCouponChild"
        case 7:
            return "numberGetOnCouponHandicapped"
        case 8:
            return "numberGetOnCommuterPass"
        case 9:
            return "numberGetOnFree"
        case 10:
            return "salesCouponAdult"
        case 11:
            return "salesCouponChild"
        case 12:
            return "salesCouponHandicapped"
        default:
            return "0"
        }
    }
    /// 選択された運賃区分と現在の停留所に応じて乗降情報を更新
    /// - Parameters:
    ///   - number: プラスボタンが押された時は"1"，マイナスボタンが押された時は"-1"
    ///   - fareID: 運賃．メソッドgetFareIDに定義している．
    func updateBoardingsInfo(number:String, fareID:String){
        //                          現時刻を取得
        let date = Date()
        let format = DateFormatter()
        format.dateFormat = "yyyy-MM-dd HH:mm:ss"
        format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
        
        
        //        乗降情報の更新
        for i in 0 ..< self.boardingsInfoDict["boardings"]!.count{
            if(self.boardingsInfoDict["boardings"]![i]["bus_stop_order"]! == String(self.selectedBusStop+1) && self.boardingsInfoDict["boardings"]![i]["fare_id"]! == fareID){
                self.boardingsInfoDict["boardings"]![i].updateValue(String(Int((Int(self.boardingsInfoDict["boardings"]![i]["number"]!) ?? 0) + (Int(number)!))), forKey: "number")
                self.boardingsInfoDict["boardings"]![i].updateValue(String(format.string(from: date)), forKey: "send_at")
            }
        }
    }
    
    /// 停留所名を取得しリターンする
    /// - Parameters:
    ///   - busStops: 停留所情報一覧
    ///   - index: index番目の停留所名を取得する
    /// - Returns: BusStopsの中にあるbus_stop_name（停留所名）
    func getBusStopName(busStops:Array<Dictionary<String,String>>, index:Int) -> String{
        return busStops[index]["bus_stop_name"]!
    }
    
    /// 到着時刻を取得しリターンする
    /// - Parameters:
    ///   - busStops: 停留所情報一覧
    ///   - index: index番目の停留所の到着時刻を取得する
    /// - Returns: BusStopsの中にあるarrival_time（到着予定時刻）
    func getArrivalTime(busStops:Array<Dictionary<String,String>>, index:Int) -> String{
        return String(busStops[index]["arrival_time"]!.prefix(5))
    }
    
    // バスのロケーションを送信する関数
    func sendBusLocation(longitude:String, latitude:String){
        //                          現時刻を取得
        let date = Date()
        
        let format = DateFormatter()
        format.dateFormat = "yyyy-MM-dd HH:mm:ss"
        format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
        
        if selectedBusStop == Int(busStops.count)-1 {
            next_stop = ""
        }
        else{
            next_stop = getBusStopName(busStops: busStops, index: selectedBusStop+1)
        }
        
        let locationDict: [String: Any] = [
            "course_id": course_id,
            "bus_id": bus_id,
            "route_order_id": String(routeOrderId),
            "bus_stop_order": String(selectedBusStop+1),
            "route_name": route,
            "longitude": longitude,
            "latitude": latitude,
            "send_at": String(format.string(from: date)),
            "vacancy_num": String(maxBoardings-self.drivedata.customoerAmount),
            "next_bus_stop_name": next_stop
        ]
        
        //        位置情報の送信
        let callAPI = CallAPI.init()
        _ = callAPI.requestData(url: "/bus/locations/create/", dict: locationDict, type: "POST")
    }
    
    /// バス停の自動切替．現在地から最も近いバス停を選択．
    /// - Parameters:
    ///   - longitude: 現在地の経度
    ///   - latitude: 現在地の緯度
    func switchBusStop(longitude: String, latitude:String){
        var distanceFromNearestBusStop:Double = distanceFrom(busStop: busStops[self.selectedBusStop], longitude:longitude, latitude: latitude)
        for i in self.autoSelectedBusStop ..< Int(busStops.count) {
            let distance:Double = distanceFrom(busStop:busStops[i], longitude: longitude, latitude: latitude)
            if(distanceFromNearestBusStop > distance){
                distanceFromNearestBusStop = distance
                self.selectedBusStop = i
                self.autoSelectedBusStop = i
            }
        }
    }
    
    /// 引数で指定したバス停から現在地までの距離を計算
    /// - Parameters:
    ///   - busStopInfo:バス停に関する情報．BusStopInfo型
    ///   - longitude: 現在地の経度
    ///   - latitude: 現在地の緯度
    /// - Returns:引数で指定したバス停から現在地までの距離
    func distanceFrom(busStop:Dictionary<String, String>, longitude: String, latitude: String) -> Double{
        let locationHere: CLLocation = CLLocation(latitude: Double(latitude)!, longitude: Double(longitude)!)
        let locationBusStop: CLLocation = CLLocation(latitude: Double(busStop["latitude"]!)!, longitude: Double(busStop["longitude"]!)!)
        return locationBusStop.distance(from: locationHere)
    }
    
    /// 引数で指定した運賃種別の人数を返す
    /// - Parameters:
    ///   - index:運行中の路線において何番目の停留所か
    ///   - row1: 乗降種別（降車数，回数券の販売数，乗車数）
    ///   - row2: 乗降者種別（現金．回数券．定期，無賃＋大人，小人，障害者）
    func getBoardingsNumber(index:Int, row1:String, row2:String) -> String{
        let boardings = self.boardingsArray[index]
        return String(boardings[row1]?[row2] ?? 0)
    }
    func getFare(fare_id: Int) -> Int{
        for i in 0..<busFare.table.count{
            for j in 0..<busFare.table[i].row2.count{
                for k in 0..<busFare.table[i].row2[j].row3.count{
                    if fare_id == Int(busFare.table[i].row2[j].row3[k]["fare_id"]!){
                        return Int(busFare.table[i].row2[j].row3[k]["amount"]!)!
                    }
                }
            }
        }
        return 0
    }
}


struct BusFare: Codable {
    var table: [Table] = [Table()]
}

struct Table: Codable {
    var row1_name:String = ""
    var row2: [Row2] = [Row2()]
}

struct Row2: Codable{
    var row2_name:String = ""
    var row3:Array<Dictionary<String, String>> = []
}

struct Success: Codable{
    var success:String = ""
}

class boardings: Object {
    @objc dynamic var route_id : String = ""
    @objc dynamic var route_order_id : String = ""
    @objc dynamic var bus_stop_id : String = ""
    @objc dynamic var fare_id : String = ""
    @objc dynamic var number : String = ""
    @objc dynamic var send_at : String = ""
    @objc dynamic var date : String = ""
}


class driveData: ObservableObject {
    
    /// 追加金額
    @Published var addAmount : Int{
        didSet {
            UserDefaults.standard.set(addAmount, forKey: "addamount")
        }
    }
    // 乗車中人数
    @Published var customoerAmount : Int{
        didSet{
            UserDefaults.standard.set( customoerAmount , forKey: "customoeramount")
        }
    }
    
    /// 初期化処理
    init() {
        addAmount = UserDefaults.standard.object(forKey: "addamount") as? Int ?? 0
        customoerAmount = UserDefaults.standard.object(forKey: "customoeramount") as? Int ?? 0
    }
}


