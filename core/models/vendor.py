# ... الحفاظ على جميع الاستيرادات السابقة ...

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    try:
        db.session.rollback()
    except:
        pass
    
    if request.method == 'POST':
        try:
            # 1. استلام البيانات من النموذج
            username = request.form.get('username')
            password = request.form.get('password')
            trade_name_val = request.form.get('trade_name')
            owner_name_val = request.form.get('owner_name')
            phone_val = request.form.get('phone')
            wallet_id = request.form.get('e_wallet') # الرقم السيادي

            # 2. رادار الفحص المسبق (Pre-flight Check)
            # فحص اسم المستخدم
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({"status": "error", "message": f"عذراً، اسم المستخدم ({username}) مسجل مسبقاً في الترسانة."})

            # فحص رقم المحفظة (الرقم السيادي)
            existing_wallet = Vendor.query.filter_by(e_wallet=wallet_id).first()
            if existing_wallet:
                return jsonify({"status": "error", "message": f"الرقم السيادي ({wallet_id}) مستخدم بالفعل لمورد آخر."})

            # 3. إنشاء حساب المستخدم
            new_user = User(username=username, role='vendor')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() 

            # 4. إنشاء بيانات المورد (مطابق تماماً لملف vendor.py)
            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=owner_name_val,
                trade_name=trade_name_val,
                phone=phone_val,
                e_wallet=wallet_id,
                # حقول إجبارية في الموديل الخاص بك أضفنا لها قيم افتراضية
                id_type=request.form.get('id_type', 'البطاقة الشخصية'),
                id_card_number=request.form.get('id_card_number', '000000'),
                activity_type=request.form.get('activity_type', 'عام'),
                province=request.form.get('province', 'الحديدة'),
                district=request.form.get('district', 'الخوخة'),
                address_detail=request.form.get('address_detail', 'الشارع العام'),
                bank_name=request.form.get('bank_name', 'بنك القطيبي'),
                bank_acc=request.form.get('bank_acc', '000000')
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم الأرشفة والتعميد السيادي بنجاح"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"تعثر تقني: {str(e)}"}), 500

    # توليد الرقم السيادي التالي (يبدأ من MAH-963)
    try:
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        next_id_num = (last_vendor.id + 1) if (last_vendor and last_vendor.id) else 963
    except:
        next_id_num = 963
        
    return render_template('add_supplier.html', next_id=f"MAH-{next_id_num}")
