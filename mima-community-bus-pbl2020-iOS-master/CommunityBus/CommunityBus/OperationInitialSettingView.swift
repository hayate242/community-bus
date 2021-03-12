import SwiftUI
import CoreLocation

var bus_id:String = ""
var course_id:String = ""
var driver_id:String = ""
var moneyAmount:String = ""
var tripMeterStartWith:String = ""


struct OperationInitialSettingView: View {
    @ObservedObject var busdata = busData()
    @Binding var isActiveOperationInitialSettingView: Bool
    @State var isActiveOperationInfoView = false
    @State var date = Date()
    @State var dateFormatter = DateFormatter()
    @State var courses = Course()
    @State var toggles = [false]
    @State var selectedCourse = 0
    @State var selectedDriverName = 0
    @State var selectedBusName = 0
    @State var remark = ""
    @State var money = ""
    var fontSize = 20
    @State var busInspection = BusInspection()
    @State var showingAlert = false
    @State var cannotGetOparationInfoAlert = false
    @State var cannotSendOperationInfoAlert = false
    @State var isNotNumberAlert = false
    @ObservedObject var locationObserver = LocationObserver()
    @State var apiErrorAlert = false
    
    func returnIndex(row: Int, column: Int) -> Int{
        return row*3 + column
    }
    
    func howManyColumn(row: Int, maxColumn: Int, items: Int) -> Int{
        if((row + 1)*maxColumn > items){
            return items % maxColumn
        }else{
            return maxColumn
        }
    }
    
    func isNumber(string: String) -> Bool {
        let pattern = "^[\\d]+$"
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return false }
        let matches = regex.matches(in: string, range: NSRange(location: 0, length: string.count))
        return matches.count > 0
    }
    
    var body: some View {
        ZStack {
            Color.gray.opacity(0.1)
                .edgesIgnoringSafeArea(.all)
            VStack {
                NavigationLink(destination: OperationInfoView(isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView),
                               isActive: $isActiveOperationInfoView) {
                    EmptyView()
                }.isDetailLink(false)
                .navigationBarTitle("運行初期設定画面", displayMode: .inline)
                .onAppear {
                    do{
                        let api = CallAPI.init()
                        
                        if monitor.currentPath.status == .unsatisfied{
                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                        }
                        
                        let jsonDataInspection = api.requestData(url: "/bus/inspections/", dict: [:], type: "GET")
                        self.busInspection = try JSONDecoder().decode(BusInspection.self, from: jsonDataInspection)
                        for _ in 0 ..< self.busInspection.item.count - 1{
                            self.toggles.append(false)
                        }
                        
                        let jsonDataCourse = api.requestData(url: "/bus/course/", dict: [:], type: "GET")
                        self.courses = try JSONDecoder().decode(Course.self, from: jsonDataCourse)
                        self.courses.Courses.append(["course_id":"","course_name":"臨時コース"])
                        
                        //                          現時刻を取得
                        dateFormatter.dateFormat = DateFormatter.dateFormat(fromTemplate: "Md", options: 0, locale: Locale(identifier: "ja_JP"))
                    }catch{
                        self.cannotGetOparationInfoAlert = true
                    }
                }.alert(isPresented: self.$cannotGetOparationInfoAlert) {
                    Alert(
                        title: Text("エラー"),
                        message: Text("業務情報の取得に失敗しました")
                    )
                }
                
                Form {
                    Section(header: Text("業務情報入力").font(.system(size: CGFloat(self.fontSize)))) {
                        HStack {
                            Text("日付").font(.system(size: CGFloat(self.fontSize)))
                            Spacer()
                            Text(dateFormatter.string(from: date)).font(.system(size: CGFloat(self.fontSize))).foregroundColor(Color.gray)
                        }
                        HStack {
                            Text("運転手名").font(.system(size: CGFloat(self.fontSize)))
                            Spacer()
                            Text(userDict.name).font(.system(size: CGFloat(self.fontSize))).foregroundColor(Color.gray)
                        }
                        Picker(selection: $selectedCourse,
                               label: Text("コース").font(.system(size: CGFloat(self.fontSize))))
                        {
                            ForEach(0..<self.courses.Courses.count){ i in
                                Text(self.courses.Courses[i]["course_name"]!)
                                    .font(.system(size: CGFloat(self.fontSize)))
                            }
                            
                        }
                        Picker(selection: $selectedBusName,
                               label: Text("車両番号")
                                .font(.system(size: CGFloat(self.fontSize))))
                        {
                            ForEach(0..<self.busInspection.buses.count){ i in
                                Text(self.busInspection.buses[i]["bus_name"]!)
                                    .font(.system(size: CGFloat(self.fontSize)))
                            }
                        }
                        HStack{
                            Text("トリップメーター(km)")
                                .font(.system(size: CGFloat(self.fontSize)))
                            TextField("ここにトリップメーターの値を入力", text: $busdata.tripMeter)
                                .multilineTextAlignment(.trailing)
                                .font(.system(size: CGFloat(self.fontSize)))
                                .keyboardType(.numberPad)
                        }
                        HStack{
                            Text("所持金額(円)")
                                .font(.system(size: CGFloat(self.fontSize)))
                            TextField("ここに所持金額を入力", text: $busdata.havingmoney)
                                .multilineTextAlignment(.trailing)
                                .font(.system(size: CGFloat(self.fontSize)))
                                .keyboardType(.numberPad)
                        }
                    }
                    
                    //                始業点検項目を生成
                    Section(header: Text("始業点検項目").font(.system(size: CGFloat(self.fontSize)))) {
                        ForEach(0..<Int(ceil(Double(self.busInspection.item.count/3))), id: \.self) {row in
                            HStack(spacing:100){
                                Group{
                                    ForEach(0 ..< self.howManyColumn(row: row, maxColumn: 3, items: self.busInspection.item.count)) {column in
                                        Toggle(isOn: self.$toggles[self.returnIndex(row: row, column: column)]){
                                            Text(self.busInspection.item[self.returnIndex(row: row, column: column)]["inspection_name"]!)
                                                .font(.system(size: CGFloat(self.fontSize)))
                                                .lineLimit(1)
                                        }
                                    }
                                }
                            }
                        }
                        HStack{
                            Text("備考欄")
                                .font(.system(size: CGFloat(self.fontSize)))
                            TextField("ここに備考を入力", text: $remark)
                                .multilineTextAlignment(.trailing)
                                .font(.system(size: CGFloat(self.fontSize)))
                        }
                    }
                    
                    
                    ZStack{
                        Button(action: {
                            for i in 0..<self.busInspection.buses.count {
                                if self.busInspection.buses[selectedBusName]["bus_name"] == self.busInspection.buses[i]["bus_name"]{
                                    bus_id = self.busInspection.buses[selectedBusName]["bus_id"]!
                                }
                            }
                            for i in 0..<self.courses.Courses.count{
                                if self.courses.Courses[selectedCourse]["course_name"] == self.courses.Courses[i]["course_name"]{
                                    course_id = self.courses.Courses[i]["course_id"]!
                                }
                            }
                            driver_id = String(userDict.id)
                            moneyAmount = String(self.busdata.havingmoney)
                            tripMeterStartWith = String(self.busdata.tripMeter)
                            
                            if(self.busdata.tripMeter == "" || self.busdata.havingmoney == ""){
                                self.showingAlert = true
                            } else if (!isNumber(string: self.busdata.tripMeter) || !isNumber(string: self.busdata.havingmoney)){
                                self.isNotNumberAlert = true
                            } else {
                                for i in 0 ..< self.busInspection.item.count{
                                    if(self.toggles[i] == false){
                                        self.showingAlert = true
                                        break
                                    }
                                }
                            }
                            
                            
                            if(self.showingAlert == false && self.isNotNumberAlert == false){
                                //                          現時刻を取得
                                let date = Date()
                                
                                let format = DateFormatter()
                                format.dateFormat = "yyyy-MM-dd HH:mm:ss"
                                format.timeZone   = TimeZone(identifier: "Asia/Tokyo")
                                
                                //                                    点検情報の送信
                                let callAPI = CallAPI.init()
                                
                                //                            送信用のデータを作成（バス点検項目）
                                let inspectionDict: [String: Any] = [
                                    "driver_id": driver_id,
                                    "bus_id": bus_id,
                                    "checked": "true",
                                    "remark": self.remark
                                ]
                                
                                do{
                                    if monitor.currentPath.status == .unsatisfied{
                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                    }
                                    let jsonDataInspections = callAPI.requestData(url: "/bus/inspections/create/", dict: inspectionDict, type: "POST")
                                    if apiErrorFlag == true{
                                        apiErrorAlert = true
                                        apiErrorFlag = false
                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                    }
                                    if jsonDataInspections.isEmpty{
                                        throw NSError(domain: "error", code: -1, userInfo: nil)
                                    }
                                    _ = try JSONDecoder().decode(Success.self, from: jsonDataInspections)
                                }catch{
                                    if self.apiErrorAlert == false{
                                        self.cannotSendOperationInfoAlert = true
                                    }
                                }
                                
                                //                            送信用のデータを作成（業務情報）
                                let initialSettingDict: [String: Any] = [
                                    "bus_id": bus_id,
                                    "driver_id": driver_id,
                                    "course_id": course_id,
                                    "trip_meter": tripMeterStartWith,
                                    "money": moneyAmount,
                                    "work_start_end_flag": "0",
                                    "send_at": String(format.string(from: date))
                                ]
                                
                                do{
                                    if monitor.currentPath.status == .unsatisfied{
                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                    }
                                    let jsonDataInit = callAPI.requestData(url: "/bus/init/create/", dict: initialSettingDict, type: "POST")
                                    if apiErrorFlag == true{
                                        apiErrorAlert = true
                                        apiErrorFlag = false
                                        throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                                    }
                                    _ = try JSONDecoder().decode(Success.self, from: jsonDataInit)
                                    self.isActiveOperationInfoView.toggle()
                                }catch{
                                    if self.apiErrorAlert == false{
                                        self.cannotSendOperationInfoAlert = true
                                    }
                                }
                            }
                        }) {
                            Text("入力完了")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .multilineTextAlignment(.trailing)
                        } .alert(isPresented: $showingAlert){
                            Alert.init(
                                title: Text("必要事項が未入力です"),
                                message: Text("トリップメーターの値・所持金額・点検項目を入力してください")
                            )
                        }
                        Text("")
                            .alert(isPresented: $isNotNumberAlert){
                                Alert(
                                    title: Text("入力エラー"),
                                    message: Text("トリップメーターと所持金額は数字のみ\n入力してください")
                                )
                            }
                        Text("")     // ダミーのView
                            .alert(isPresented: self.$cannotSendOperationInfoAlert){
                                Alert(
                                    title: Text("通信エラー"),
                                    message: Text("業務情報を送信できませんでした")
                                )
                            }
                        Text("")     // ダミーのView
                            .alert(isPresented: $apiErrorAlert){
                                Alert(
                                    title: Text("送信に失敗しました"),
                                    message: Text("もう一度お試しください")
                                )
                            }
                    }
                }
            }.frame(maxWidth: UIScreen.main.bounds.width * 4 / 5)
        }
    }
}

struct BusInspection: Codable {
    var drivers: Array<Dictionary<String, String>> = []
    var buses: Array<Dictionary<String, String>> = []
    var item: Array<Dictionary<String, String>> = []
}

struct Course: Codable {
    var Courses: Array<Dictionary<String, String>> = []
}

class busData: ObservableObject {
    
    /// トリップメーター
    @Published var tripMeter : String {
        didSet {
            UserDefaults.standard.set(tripMeter, forKey: "tripmeter")
        }
    }
    // 所持金額
    @Published var havingmoney : String{
        didSet{
            UserDefaults.standard.set(havingmoney, forKey: "havingmoney")
        }
    }
    
    /// 初期化処理
    init() {
        tripMeter = UserDefaults.standard.string(forKey: "tripmeter") ?? ""
        havingmoney = UserDefaults.standard.string(forKey: "havingmoney") ?? ""
    }
}


