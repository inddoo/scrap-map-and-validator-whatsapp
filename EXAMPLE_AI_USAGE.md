# 📝 Example AI Usage - Step by Step

## Scenario 1: Sales Outreach Campaign

### Goal
Kirim pesan promosi personal ke 50 prospek dari berbagai perusahaan.

### Steps

#### 1. Prepare CSV Data
Create `sales_prospects.csv`:
```csv
phone,name,company,position,industry,pain_point
628123456789,John Doe,PT ABC Tech,CEO,Technology,Manual processes
628987654321,Jane Smith,CV XYZ,Marketing Manager,Retail,Low online presence
628555666777,Bob Johnson,UD 123,Owner,F&B,Inventory management
```

#### 2. Upload CSV
- Go to "📨 WA Auto Sender" tab
- Click "📤 Upload CSV"
- Select `sales_prospects.csv`
- ✅ CSV loaded with 3 contacts

#### 3. Enable AI
- Check ✅ "Gunakan AI untuk Generate Pesan Personal"

#### 4. Write AI Template
```
Buatkan pesan sales untuk {name} yang bekerja sebagai {position} di {company}.

Konteks:
- Industri mereka: {industry}
- Pain point: {pain_point}

Pesan harus:
1. Sapa dengan nama dan jabatan
2. Tunjukkan pemahaman tentang industri mereka
3. Sebutkan pain point mereka
4. Tawarkan solusi kami (software automation)
5. Ajak untuk meeting/demo
6. Profesional tapi ramah
7. Gunakan emoji yang sesuai

Jangan terlalu panjang (max 4 paragraf).
```

#### 5. Add Context (Optional)
```
Kami adalah PT Digital Solutions, perusahaan software house yang fokus pada automation dan digitalisasi bisnis. 
Produk kami: ERP, CRM, Inventory Management, POS System.
Sudah dipercaya 100+ perusahaan di Indonesia.
```

#### 6. Generate AI Messages
- Click "🤖 Generate Pesan AI"
- Wait 10-30 seconds
- ✅ 3 messages generated

#### 7. Review Generated Messages
Preview akan muncul:
```
✅ Pesan AI Berhasil Digenerate (3)

John Doe - PT ABC Tech:
"Halo Pak John! 👋

Saya dari PT Digital Solutions. Saya memahami bahwa di industri Technology, 
manual processes bisa sangat menghambat produktivitas...
[Read more]"
```

#### 8. Enable Auto Responder (Optional)
- Check ✅ "Aktifkan Auto Responder AI"
- Set prompt:
```
Anda adalah sales consultant yang profesional.
Jika prospek bertanya tentang harga, jelaskan bahwa harga custom sesuai kebutuhan.
Jika prospek tertarik, tawarkan meeting/demo.
Jika prospek menolak, ucapkan terima kasih dan tawarkan untuk follow up nanti.
Selalu ramah dan tidak pushy.
```

#### 9. Set Delay
- Min: 8 seconds
- Max: 15 seconds

#### 10. Send Messages
- Click "🤖 Kirim Pesan AI (3 nomor)"
- Monitor progress
- ✅ Done!

---

## Scenario 2: Event Invitation

### Goal
Undang 100 profesional ke webinar tentang Digital Marketing.

### CSV Data
```csv
phone,name,company,position,interest
628111,Alice,PT AAA,Marketing Head,Social Media
628222,Bob,CV BBB,CEO,SEO
628333,Charlie,UD CCC,Owner,Content Marketing
```

### AI Template
```
Undang {name} ({position}) dari {company} ke webinar kami.

Detail webinar:
- Topik: "Digital Marketing Trends 2024"
- Tanggal: 20 Maret 2024
- Waktu: 14:00 - 16:00 WIB
- Platform: Zoom
- Gratis + Sertifikat

Sesuaikan dengan interest mereka: {interest}

Pesan harus:
1. Personal dan menyapa nama
2. Jelaskan benefit webinar untuk mereka
3. Highlight topik yang sesuai interest mereka
4. Ajak untuk register
5. Sertakan link register (gunakan bit.ly/webinar-dm2024)
6. Enthusiastic tapi profesional
```

### Expected Output
```
Halo Ibu Alice! 👋

Kami mengundang Ibu untuk webinar "Digital Marketing Trends 2024" 
khusus untuk Marketing Heads seperti Ibu.

Topik spesial untuk Ibu:
📱 Social Media Marketing Strategies 2024
📊 Analytics & ROI Measurement
🎯 Audience Targeting Techniques

📅 20 Maret 2024, 14:00 WIB
💻 Via Zoom
🎓 Gratis + Sertifikat

Daftar sekarang: bit.ly/webinar-dm2024

Sampai jumpa! 😊
```

---

## Scenario 3: Customer Follow-Up

### Goal
Follow up 30 customers yang sudah meeting tapi belum closing.

### CSV Data
```csv
phone,name,company,meeting_date,topic,status
628111,David,PT DDD,2024-03-01,ERP Implementation,Considering
628222,Emma,CV EEE,2024-02-28,CRM System,Need approval
628333,Frank,UD FFF,2024-02-25,POS System,Budget issue
```

### AI Template
```
Follow up {name} dari {company} tentang meeting terakhir tanggal {meeting_date}.

Topik meeting: {topic}
Status terakhir: {status}

Pesan harus:
1. Ingatkan tentang meeting terakhir
2. Tanyakan apakah ada pertanyaan atau concern
3. Tawarkan bantuan sesuai status mereka
4. Jika budget issue, tawarkan payment plan
5. Jika need approval, tawarkan presentasi ke decision maker
6. Jika considering, berikan case study/testimonial
7. Soft selling, tidak pushy
8. Ajak untuk next step yang jelas
```

### Auto Responder Prompt
```
Anda adalah account manager yang membantu customer.

Jika customer bertanya teknis: Jelaskan dengan detail atau tawarkan demo.
Jika customer minta diskon: Jelaskan value proposition, tawarkan payment plan.
Jika customer butuh approval: Tawarkan presentasi ke decision maker.
Jika customer menunda: Tanyakan timeline yang sesuai, tawarkan follow up.

Selalu solution-oriented dan helpful.
```

---

## Scenario 4: Appointment Reminder

### Goal
Reminder appointment besok ke 20 klien.

### CSV Data
```csv
phone,name,appointment_date,appointment_time,service,location
628111,Grace,2024-03-06,10:00,Konsultasi,Office
628222,Henry,2024-03-06,14:00,Demo,Zoom
628333,Ivy,2024-03-06,16:00,Training,Client Office
```

### AI Template
```
Reminder appointment untuk {name} besok.

Detail:
- Tanggal: {appointment_date}
- Waktu: {appointment_time}
- Layanan: {service}
- Lokasi: {location}

Pesan harus:
1. Friendly reminder
2. Konfirmasi detail appointment
3. Jika office, berikan alamat dan parking info
4. Jika zoom, berikan link meeting
5. Minta konfirmasi kehadiran
6. Berikan contact person jika ada pertanyaan
7. Professional tapi warm
```

---

## Tips for Best Results

### 1. Template Writing
✅ **Good Template:**
```
Buatkan pesan untuk {name} dari {company}.
Tawarkan produk X dengan benefit Y.
Sesuaikan dengan industri mereka: {industry}.
Gunakan tone profesional tapi ramah.
Max 3 paragraf.
```

❌ **Bad Template:**
```
Halo {name}, kami punya produk bagus.
```

### 2. CSV Data Quality
✅ **Good CSV:**
- Complete data (name, company, position)
- Relevant fields (industry, pain_point, interest)
- Clean phone numbers (628xxx format)

❌ **Bad CSV:**
- Missing data
- Irrelevant fields
- Wrong phone format

### 3. Context Usage
✅ **Good Context:**
```
Kami adalah PT ABC, fokus pada automation software.
Produk: ERP, CRM, POS.
Target: SME di Indonesia.
USP: Affordable, easy to use, local support.
```

❌ **Bad Context:**
```
Kami perusahaan bagus.
```

### 4. Auto Responder Prompts
✅ **Good Prompt:**
```
Anda adalah customer service.
Jika tanya harga: Jelaskan pricing model.
Jika tanya fitur: Jelaskan dengan detail.
Jika komplain: Empati dan tawarkan solusi.
Tone: Professional, helpful, patient.
```

❌ **Bad Prompt:**
```
Jawab pertanyaan customer.
```

---

## Monitoring & Optimization

### Track Results
1. Monitor send success rate
2. Track response rate
3. Analyze which templates work best
4. A/B test different approaches

### Optimize
1. Refine templates based on responses
2. Update auto responder prompts
3. Adjust delay timing
4. Segment audience better

---

## Safety Checklist

Before sending:
- [ ] Test with 1-2 numbers first
- [ ] Review generated messages
- [ ] Check phone numbers format
- [ ] Set appropriate delay (min 5-10 sec)
- [ ] Comply with WhatsApp ToS
- [ ] Respect privacy & GDPR
- [ ] Have opt-out mechanism
- [ ] Monitor for spam reports

---

**Happy Automating! 🚀**

For more info: [AI_FEATURES_GUIDE.md](backend/AI_FEATURES_GUIDE.md)
