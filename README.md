# MVC2-68: Rumour Tracking System

ระบบตติดตามข่าวลือแบบ MVC Pattern สำหรับรายงานและตรวจสอบข่าวลือ

## 🎯 Features

- **Login System**: ระบบเข้าสู่ระบบด้วย User ID
- **Rumour Management**: ดู รายการข่าวลือทั้งหมด พร้อมสถานะและจำนวนรายงาน
- **Report System**: ผู้ใช้ทั่วไปสามารถรายงานข่าวลือได้ (ข้อมูลเท็จ, ปลุกปั่น, บิดเบือน)
- **Verification System**: ผู้ตรวจสอบสามารถยืนยันความจริงของข่าวลือได้
- **Summary Dashboard**: แสดงสรุปข่าวลือแบ่งเป็น Panic, Verified True, Verified False
- **Panic Threshold**: ข่าวลือที่ถูกรายงาน 3 ครั้งขึ้นไปจะเปลี่ยนสถานะเป็น "panic"

## 🏗️ Architecture

โปรเจ็กต์ปฏิบัติตาม **MVC Pattern** อย่างเคร่งครัด:

```
MVC2-68/
├── Controllers/
│   └── app_controller.py    # Business logic และ orchestration
├── Models/
│   ├── rumour_model.py       # Rumour data management
│   ├── report_model.py       # Report tracking
│   └── user_model.py         # User authentication
├── Views/
│   ├── login_view.py         # Login interface
│   ├── rumour_list_view.py   # Rumour list display
│   ├── rumour_detail_view.py # Detail + reporting interface
│   └── summary_view.py       # Summary dashboard
├── Data/
│   ├── rumours.json          # Rumour data
│   ├── reports.json          # Report records
│   └── users.json            # User accounts
├── config.py                 # Configuration constants
└── main.py                   # Application entry point
```

## 🚀 Installation

### Requirements
- Python 3.8+
- Tkinter (มักติดตั้งมาพร้อม Python)

### Setup
```bash
# Clone repository
git clone git@github.com:Puiluiz/MVC2-68.git
cd MVC2-68

# Run application
python main.py
```

## 👥 User Accounts

### Regular Users (ผู้ใช้่วไป)
- U0001, U0003, U0005, U0006, U0008, U0009, etc.
- สามารถ: ดูข่าวลือ, รายงานข่าวลือ

### Inspectors (ผู้ตรวจสอบ)
- U0002, U0004, U0007, U0010, U0012, etc.
- สามารถ: ทำทุกอย่างที่ผู้ใช้ทั่วไปทำได้ + ยืนยันความจริงของข่าวลือ

## 📊 Business Rules

1. **Panic Threshold**: ข่าวลือที่ถูกรายงาน ≥ 3 ครั้ง → สถานะเปลี่ยนเป็น "panic"
2. **Duplicate Prevention**: ผู้ใช้แต่ละคนรายงานข่าวลือแต่ละข่าวได้เพียง 1 ครั้ง
3. **Verification Lock**: ข่าวลือที่ยืนยันแล้วจะไม่สามารถรายงานเพิ่มได้
4. **Role-Based Access**: เฉพาะ Inspector เท่านั้นที่ตรวจสอบข่าวลือได้

## 💎 Code Quality

- ✅ **Type Hints**: 100% coverage
- ✅ **Docstrings**: ครบทุก class และ public method
- ✅ **MVC Pattern**: แยก layer ชัดเจน ไม่มี violations
- ✅ **Error Handling**: Comprehensive validation
- ✅ **No Dependencies**: ใช้เฉพาะ Python standard library

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

Developed as part of MVC architecture learning project.
