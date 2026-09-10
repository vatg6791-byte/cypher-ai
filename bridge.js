async function sendToCypherCore(userText) {
    const url = `${CONFIG.API_URL}?key=${CONFIG.API_KEY}`;
    
    // دمج الرومبت الفولاذي مع نص المستخدم لضمان التنفيذ الفوري
    const combinedPayload = SYSTEM_PROMPT + "\n\n[USER COMMAND]: " + userText;

    const bodyData = {
        contents: [
            {
                parts: [
                    { text: combinedPayload }
                ]
            }
        ]
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0].content.parts[0].text) {
            return data.candidates[0].content.parts[0].text;
        } else if (data.error) {
            return "خطأ في استجابة العقل: " + data.error.message;
        } else {
            return "استجابة غير صالحة من النظام.";
        }
    } catch (err) {
        return "فشل الاتصال بالخادم أو الشبكة.";
    }
}
