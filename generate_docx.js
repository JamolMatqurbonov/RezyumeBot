const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, VerticalAlign, ImageRun } = require('docx');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

const FONT = "Times New Roman";
const SIZE = 28; // 14pt = 28 half-points

const val = (v) => (v && String(v).trim() !== '' && v !== 'undefined') ? String(v).trim() : 'йўқ';

// ─── Chegara ───
const border = {
    top:    { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    left:   { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    right:  { style: BorderStyle.SINGLE, size: 4, color: "000000" },
};

// ─── Katak yasash ───
const C = (text, opts = {}) => new TableCell({
    width: opts.w ? { size: opts.w, type: WidthType.DXA } : { size: 1, type: WidthType.AUTO },
    columnSpan: opts.span || 1,
    rowSpan: opts.rs || 1,
    verticalAlign: VerticalAlign.CENTER,
    shading: opts.gray ? { fill: "D9D9D9" } : undefined,
    borders: border,
    children: [new Paragraph({
        alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
            text: String(text ?? 'йўқ'),
            bold: opts.bold || false,
            size: SIZE,
            font: FONT,
        })]
    })]
});

// ─── Rasm katagi ───
let rasmCell;
if (data.rasm_path && fs.existsSync(data.rasm_path)) {
    try {
        const imgBuf = fs.readFileSync(data.rasm_path);
        rasmCell = new TableCell({
            rowSpan: 9,
            width: { size: 1800, type: WidthType.DXA },
            verticalAlign: VerticalAlign.CENTER,
            borders: border,
            children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new ImageRun({ data: imgBuf, transformation: { width: 95, height: 125 }, type: "jpg" })]
            })]
        });
    } catch(e) {
        rasmCell = C('3×4', { rs: 9, center: true });
    }
} else {
    rasmCell = C('3×4 ФОТО', { rs: 9, center: true });
}

// ─── FIO ───
const fio = [data.familya, data.ism, data.otasining_ismi]
    .map(s => (s || '').trim())
    .filter(Boolean)
    .join(' ')
    .toUpperCase() || 'йўқ';

// ─── Oila satrlari ───
const oilaRows = (data.oila || []).map(a => new TableRow({ children: [
    C(val(a.qarindoshligi)),
    C(val(a.ismi)),
    C(val(a.yili)),
    C(val(a.ish_joyi)),
    C(val(a.manzil)),
]}));

if (oilaRows.length === 0) {
    oilaRows.push(new TableRow({ children: [C('йўқ'), C('йўқ'), C('йўқ'), C('йўқ'), C('йўқ')] }));
}

// ─── Mehnat faoliyati satrlari ───
const ishRows = [];
if (data.ish_joyi && data.ish_joyi.trim()) {
    ishRows.push(new TableRow({ children: [
        C(val(data.ish_yillari)),
        C(`${val(data.ish_joyi)} — ${val(data.lavozim)}`),
    ]}));
}
if (ishRows.length === 0) {
    ishRows.push(new TableRow({ children: [C('йўқ'), C('йўқ')] }));
}

// ─── Paragraph yordamchi ───
const P = (text, opts = {}) => new Paragraph({
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
    spacing: { before: opts.before || 0, after: opts.after || 0 },
    children: [new TextRun({ text: String(text), bold: opts.bold || false, size: SIZE, font: FONT })]
});

// ─── HUJJAT ───
const doc = new Document({
    styles: {
        default: { document: { run: { font: FONT, size: SIZE } } }
    },
    sections: [{
        properties: {
            page: {
                size: { width: 11906, height: 16838 },
                margin: { top: 720, right: 720, bottom: 720, left: 1440 }
            }
        },
        children: [

            // SARLAVHA
            P("МАЪЛУМОТНОМА", { center: true, bold: true, after: 200 }),

            // ASOSIY JADVAL
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    // 1: FIO
                    new TableRow({ children: [
                        C(fio, { span: 2, center: true, bold: true }),
                        rasmCell,
                    ]}),
                    // 2: Tug'ilgan sana + joy
                    new TableRow({ children: [
                        C(`Туғилган йили: ${val(data.tugilgan_sana)}`),
                        C(`Туғилган жойи: ${val(data.tugilgan_joy)}`),
                    ]}),
                    // 3: Millat + partiya
                    new TableRow({ children: [
                        C(`Миллати: ${val(data.millati)}`),
                        C(`Партиявийлиги: ${val(data.partiya)}`),
                    ]}),
                    // 4: Ma'lumot + tamomlagan
                    new TableRow({ children: [
                        C(`Маълумоти: ${val(data.malumot)}`),
                        C(`Тамомлаган: ${val(data.tamomlagan)} й. ${val(data.okuw_joyi)}`),
                    ]}),
                    // 5: Mutaxassislik
                    new TableRow({ children: [
                        C("Маълумоти бўйича мутахассислиги:"),
                        C(val(data.mutaxassislik)),
                    ]}),
                    // 6: Ilmiy
                    new TableRow({ children: [
                        C("Илмий даражаси: йўқ"),
                        C("Илмий унвони: йўқ"),
                    ]}),
                    // 7: Tillar
                    new TableRow({ children: [
                        C(`Қайси чет тилларини билади: ${val(data.tillar)}`, { span: 2 }),
                    ]}),
                    // 8: Telefon + email
                    new TableRow({ children: [
                        C(`Телефон: ${val(data.telefon)}`),
                        C(`E-mail: ${val(data.email)}`),
                    ]}),
                    // 9: Manzil
                    new TableRow({ children: [
                        C(`Яшаш манзили: ${val(data.manzil)}`, { span: 2 }),
                    ]}),
                    // 10: Mukofotlar (rasm yo'q, shu yerdan 2 ustun)
                    new TableRow({ children: [
                        C(`Давлат мукофотлари: ${val(data.mukofotlar)}`, { span: 3 }),
                    ]}),
                    // 11: Deputat
                    new TableRow({ children: [
                        C("Халқ депутатлари советининг аъзосими: йўқ", { span: 3 }),
                    ]}),
                ]
            }),

            // MEHNAT FAOLIYATI
            P("", { before: 200 }),
            P("МЕҲНАТ ФАОЛИЯТИ", { center: true, bold: true, after: 100 }),

            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({ children: [
                        C("Йиллар", { bold: true, center: true, w: 2500 }),
                        C("Иш жойи ва лавозими", { bold: true, center: true }),
                    ]}),
                    ...ishRows,
                ]
            }),

            // OILA
            P("", { before: 200 }),
            P("ЯҚИН ҚАРИНДОШЛАРИ ҲАҚИДА МАЪЛУМОТ", { center: true, bold: true, after: 100 }),

            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({ children: [
                        C("Қариндош-лиги",              { bold: true, center: true }),
                        C("Фамилияси, исми ва отасининг исми", { bold: true, center: true }),
                        C("Туғилган йили ва жойи",      { bold: true, center: true }),
                        C("Иш жойи ва лавозими",        { bold: true, center: true }),
                        C("Яшаш жойи",                  { bold: true, center: true }),
                    ]}),
                    ...oilaRows,
                ]
            }),

            // Qo'shimcha
            ...(data.qoshimcha && data.qoshimcha.trim()
                ? [P("", { before: 200 }), P(`Қўшимча: ${data.qoshimcha}`)]
                : []
            ),

            // Sana + imzo
            P("", { before: 400 }),
            P(`Сана: ${new Date().toLocaleDateString('uz-UZ')}`),
            P(`Имзо: _______________________ ${val(data.familya)} ${(val(data.ism)[0] || '')}.${(val(data.otasining_ismi)[0] || '')}.`),
        ]
    }]
});

Packer.toBuffer(doc).then(buf => {
    fs.writeFileSync(process.argv[3], buf);
    console.log('OK:' + process.argv[3]);
}).catch(e => {
    console.error('ERROR:' + e.message);
    process.exit(1);
});
