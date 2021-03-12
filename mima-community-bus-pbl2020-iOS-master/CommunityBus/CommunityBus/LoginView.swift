import SwiftUI
import Network

var userDict = User()
let monitor = NWPathMonitor()
let queue = DispatchQueue(label: "Monitor")

struct LoginView: View {
    @ObservedObject var profile = UserData()
    @State var inputID: String = ""
    @State var inputPassword: String = ""
    @State var errorMessage: String = ""
    @State var isActiveOperationInitialSettingView = false
    @State var tokenDict = Token()
    @State var communicationAlert = false
    @State var apiErrorAlert = false
    
    var body: some View {
        NavigationView {
            VStack(alignment: .center,spacing: UIScreen.main.bounds.height/32) {
                Text("三間地区コミュニティバス\n乗降者数管理システム")
                    .font(.system(size: 48,
                                  weight: .heavy))
                    .frame(height: UIScreen.main.bounds.height * 8 / 32)
                    .multilineTextAlignment(.center)
                    .fixedSize()
                
                Text(errorMessage)
                    .foregroundColor(Color.red)
                    .frame(height: UIScreen.main.bounds.height / 32)
                
                TextField("ユーザーID", text: $profile.userid)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(maxWidth: 500)
                    .frame(height: UIScreen.main.bounds.height / 32)
                
                SecureField("パスワード", text: $inputPassword)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(maxWidth: 500)
                    .frame(height: UIScreen.main.bounds.height / 32)
                
                VStack {
                    //コード上のイベントで遷移したい場合は、LabelにEmptyViewを指定する
                    NavigationLink(destination: OperationInitialSettingView( isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView),
                                   isActive: $isActiveOperationInitialSettingView) {
                        EmptyView()
                    }
                    .onAppear {
                        monitor.start(queue: queue)
                    }
                    Button(action: {
                        //                        トークンのダミーデータをuserdefaultで保存
                        if let encodedValue = try? JSONEncoder().encode(self.tokenDict) {
                            UserDefaults.standard.set(encodedValue, forKey: "token")
                        }
                        let callAPI = CallAPI.init()
                        
                        //            トークンの取得
                        let tokenDict: [String: Any] = [
                            "email": self.profile.userid,
                            "password": self.inputPassword
                        ]
                        
                        do{
                            if monitor.currentPath.status == .unsatisfied{
                                communicationAlert = true
                                throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                            }
                            let jsonDataToken = callAPI.requestData(url: "/login/", dict: tokenDict, type: "POST")
                            if apiErrorFlag == true{
                                apiErrorAlert = true
                                apiErrorFlag = false
                                throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                            }
                            self.tokenDict = try JSONDecoder().decode(Token.self, from: jsonDataToken)
                            
                            //                        トークンの保存
                            if let encodedValue = try? JSONEncoder().encode(self.tokenDict) {
                                UserDefaults.standard.set(encodedValue, forKey: "token")
                            }
                            //                        ユーザ情報の取得
                            let jsonDataUser = callAPI.requestData(url: "/user/info/", dict: [:], type: "GET")
                            
                            userDict = try JSONDecoder().decode(User.self, from: jsonDataUser)
                            self.errorMessage = ""
                            self.isActiveOperationInitialSettingView.toggle()
                            
                        } catch{
                            if communicationAlert == false && apiErrorAlert == false{
                                self.errorMessage = "IDまたはパスワードが間違っています"
                            }
                        }
                    },
                    label: {
                        Text("ログイン")
                            .fontWeight(.medium)
                            .frame(minWidth: 160)
                            .foregroundColor(.white)
                            .padding(12)
                            .background(Color.accentColor)
                            .cornerRadius(8)
                            .padding(UIScreen.main.bounds.height / 32)
                    })
                }.alert(isPresented: $communicationAlert){
                    Alert.init(
                        title: Text("通信エラー"),
                        message: Text("アカウント情報の送信に失敗しました"))
                }
                Text("")
                    .alert(isPresented: $apiErrorAlert){
                        Alert(
                            title: Text("送信に失敗しました"),
                            message: Text("もう一度お試しください")
                        )
                    }
                
            }
            .navigationBarTitle("ログイン画面", displayMode: .inline)
        }.navigationViewStyle(StackNavigationViewStyle())
    }
}

class UserData: ObservableObject {
    /// ユーザ名
    @Published var userid: String {
        didSet {
            UserDefaults.standard.set(userid, forKey: "userid")
        }
    }
    /// 初期化処理
    init() {
        userid = UserDefaults.standard.string(forKey: "userid") ?? ""
    }
}





struct Token: Codable{
    var access_token: String = ""
    var token_type: String = ""
    var expire_in: Int = 0
}

struct User: Codable {
    var id: String = ""
    var name: String = ""
    var phone_number: String = ""
    var email: String = ""
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
    }
}
