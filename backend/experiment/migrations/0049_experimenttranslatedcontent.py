# Generated by Django 4.2.14 on 2024-07-31 13:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import experiment.models


class Migration(migrations.Migration):
    dependencies = [
        ("experiment", "0048_block_phase_delete_groupedblock"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExperimentTranslatedContent",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("index", models.IntegerField(default=0)),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Unset"),
                            ("aa", "Afar"),
                            ("af", "Afrikaans"),
                            ("ak", "Akan"),
                            ("sq", "Albanian"),
                            ("am", "Amharic"),
                            ("ar", "Arabic"),
                            ("an", "Aragonese"),
                            ("hy", "Armenian"),
                            ("as", "Assamese"),
                            ("av", "Avaric"),
                            ("ae", "Avestan"),
                            ("ay", "Aymara"),
                            ("az", "Azerbaijani"),
                            ("bm", "Bambara"),
                            ("ba", "Bashkir"),
                            ("eu", "Basque"),
                            ("be", "Belarusian"),
                            ("bn", "Bengali"),
                            ("bh", "Bihari languages"),
                            ("bi", "Bislama"),
                            ("nb", "Bokmål, Norwegian; Norwegian Bokmål"),
                            ("bs", "Bosnian"),
                            ("br", "Breton"),
                            ("bg", "Bulgarian"),
                            ("my", "Burmese"),
                            ("ca", "Catalan; Valencian"),
                            ("km", "Central Khmer"),
                            ("ch", "Chamorro"),
                            ("ce", "Chechen"),
                            ("ny", "Chichewa; Chewa; Nyanja"),
                            ("zh", "Chinese"),
                            ("cu", "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic"),
                            ("cv", "Chuvash"),
                            ("kw", "Cornish"),
                            ("co", "Corsican"),
                            ("cr", "Cree"),
                            ("hr", "Croatian"),
                            ("cs", "Czech"),
                            ("da", "Danish"),
                            ("dv", "Divehi; Dhivehi; Maldivian"),
                            ("nl", "Dutch; Flemish"),
                            ("dz", "Dzongkha"),
                            ("en", "English"),
                            ("eo", "Esperanto"),
                            ("et", "Estonian"),
                            ("ee", "Ewe"),
                            ("fo", "Faroese"),
                            ("fj", "Fijian"),
                            ("fi", "Finnish"),
                            ("fr", "French"),
                            ("ff", "Fulah"),
                            ("gd", "Gaelic; Scottish Gaelic"),
                            ("gl", "Galician"),
                            ("lg", "Ganda"),
                            ("ka", "Georgian"),
                            ("de", "German"),
                            ("el", "Greek, Modern (1453-)"),
                            ("gn", "Guarani"),
                            ("gu", "Gujarati"),
                            ("ht", "Haitian; Haitian Creole"),
                            ("ha", "Hausa"),
                            ("he", "Hebrew"),
                            ("hz", "Herero"),
                            ("hi", "Hindi"),
                            ("ho", "Hiri Motu"),
                            ("hu", "Hungarian"),
                            ("is", "Icelandic"),
                            ("io", "Ido"),
                            ("ig", "Igbo"),
                            ("id", "Indonesian"),
                            ("ia", "Interlingua (International Auxiliary Language Association)"),
                            ("ie", "Interlingue; Occidental"),
                            ("iu", "Inuktitut"),
                            ("ik", "Inupiaq"),
                            ("ga", "Irish"),
                            ("it", "Italian"),
                            ("ja", "Japanese"),
                            ("jv", "Javanese"),
                            ("kl", "Kalaallisut; Greenlandic"),
                            ("kn", "Kannada"),
                            ("kr", "Kanuri"),
                            ("ks", "Kashmiri"),
                            ("kk", "Kazakh"),
                            ("ki", "Kikuyu; Gikuyu"),
                            ("rw", "Kinyarwanda"),
                            ("ky", "Kirghiz; Kyrgyz"),
                            ("kv", "Komi"),
                            ("kg", "Kongo"),
                            ("ko", "Korean"),
                            ("kj", "Kuanyama; Kwanyama"),
                            ("ku", "Kurdish"),
                            ("lo", "Lao"),
                            ("la", "Latin"),
                            ("lv", "Latvian"),
                            ("li", "Limburgan; Limburger; Limburgish"),
                            ("ln", "Lingala"),
                            ("lt", "Lithuanian"),
                            ("lu", "Luba-Katanga"),
                            ("lb", "Luxembourgish; Letzeburgesch"),
                            ("mk", "Macedonian"),
                            ("mg", "Malagasy"),
                            ("ms", "Malay"),
                            ("ml", "Malayalam"),
                            ("mt", "Maltese"),
                            ("gv", "Manx"),
                            ("mi", "Maori"),
                            ("mr", "Marathi"),
                            ("mh", "Marshallese"),
                            ("mn", "Mongolian"),
                            ("na", "Nauru"),
                            ("nv", "Navajo; Navaho"),
                            ("nd", "Ndebele, North; North Ndebele"),
                            ("nr", "Ndebele, South; South Ndebele"),
                            ("ng", "Ndonga"),
                            ("ne", "Nepali"),
                            ("se", "Northern Sami"),
                            ("no", "Norwegian"),
                            ("nn", "Norwegian Nynorsk; Nynorsk, Norwegian"),
                            ("oc", "Occitan (post 1500)"),
                            ("oj", "Ojibwa"),
                            ("or", "Oriya"),
                            ("om", "Oromo"),
                            ("os", "Ossetian; Ossetic"),
                            ("pi", "Pali"),
                            ("pa", "Panjabi; Punjabi"),
                            ("fa", "Persian"),
                            ("pl", "Polish"),
                            ("pt", "Portuguese"),
                            ("ps", "Pushto; Pashto"),
                            ("qu", "Quechua"),
                            ("ro", "Romanian; Moldavian; Moldovan"),
                            ("rm", "Romansh"),
                            ("rn", "Rundi"),
                            ("ru", "Russian"),
                            ("sm", "Samoan"),
                            ("sg", "Sango"),
                            ("sa", "Sanskrit"),
                            ("sc", "Sardinian"),
                            ("sr", "Serbian"),
                            ("sn", "Shona"),
                            ("ii", "Sichuan Yi; Nuosu"),
                            ("sd", "Sindhi"),
                            ("si", "Sinhala; Sinhalese"),
                            ("sk", "Slovak"),
                            ("sl", "Slovenian"),
                            ("so", "Somali"),
                            ("st", "Sotho, Southern"),
                            ("es", "Spanish; Castilian"),
                            ("su", "Sundanese"),
                            ("sw", "Swahili"),
                            ("ss", "Swati"),
                            ("sv", "Swedish"),
                            ("tl", "Tagalog"),
                            ("ty", "Tahitian"),
                            ("tg", "Tajik"),
                            ("ta", "Tamil"),
                            ("tt", "Tatar"),
                            ("te", "Telugu"),
                            ("th", "Thai"),
                            ("bo", "Tibetan"),
                            ("ti", "Tigrinya"),
                            ("to", "Tonga (Tonga Islands)"),
                            ("ts", "Tsonga"),
                            ("tn", "Tswana"),
                            ("tr", "Turkish"),
                            ("tk", "Turkmen"),
                            ("tw", "Twi"),
                            ("ug", "Uighur; Uyghur"),
                            ("uk", "Ukrainian"),
                            ("ur", "Urdu"),
                            ("uz", "Uzbek"),
                            ("ve", "Venda"),
                            ("vi", "Vietnamese"),
                            ("vo", "Volapük"),
                            ("wa", "Walloon"),
                            ("cy", "Welsh"),
                            ("fy", "Western Frisian"),
                            ("wo", "Wolof"),
                            ("xh", "Xhosa"),
                            ("yi", "Yiddish"),
                            ("yo", "Yoruba"),
                            ("za", "Zhuang; Chuang"),
                            ("zu", "Zulu"),
                        ],
                        default="",
                        max_length=2,
                    ),
                ),
                ("name", models.CharField(default="", max_length=64)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "consent",
                    models.FileField(
                        blank=True,
                        default="",
                        upload_to=experiment.models.consent_upload_path,
                        validators=[django.core.validators.FileExtensionValidator(allowed_extensions=["md", "html"])],
                    ),
                ),
                ("about_content", models.TextField(blank=True, default="")),
                (
                    "experiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translated_content",
                        to="experiment.experiment",
                    ),
                ),
            ],
        ),
    ]
