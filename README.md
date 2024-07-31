# Project 名: Smart Menu Planner

## プロジェト概要
目的：手軽に週間献立の生成及び利用客の予測による食材管理の効率化
- 大学学生食堂のメニュー管理が簡単にできます。
- 登録されたメニューで週間献立を生成できます。
- 生成された献立を基盤にして利用客を予測し、必要な食材量を計算できます。

## Flow chart
![SmartMenuPlanner_Flowchart](https://github.com/user-attachments/assets/b057b3ff-3a18-4370-8f22-d8dded8e29f7)

## EDR
<img width="760" alt="스크린샷 2024-07-31 오후 1 48 04" src="https://github.com/user-attachments/assets/e25a565a-2931-4ff8-9e15-75730286c367">

## Projectに使った技術
FrontEnd :　HTML, bootstrap, JS   
BackEnd : Django    
DB : sqlite3 -> MySQL    
version management : git    

## 改善事項
- urlconf再設計　：　メンテナンス及び拡張性の向上
- test.py　作成
- Post Detail page 修正　：　登録されたレシピと材料を画面に出力

## 開発予定
- Weekly Meal Appを Web Systemに具現
- 発注量予測機能具現
-　実査表生成機能具現
- 必要な食材発注量計算機能具現
- メイン画面構成具現
- 発注量テーブルをexel fileで保存する機能具現
