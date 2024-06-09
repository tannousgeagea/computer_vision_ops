class Emoji:
    # Define emoji symbols as a dictionary
    emoji_dict = {
        "grinning_face": "😀",
        "grinning_face_big_eyes": "😃",
        "grinning_face_smiling_eyes": "😄",
        "beaming_face_smiling_eyes": "😁",
        "grinning_squinting_face": "😆",
        "grinning_face_sweat": "😅",
        "rolling_on_floor_laughing": "🤣",
        "face_tears_of_joy": "😂",
        "slightly_smiling_face": "🙂",
        "upside_down_face": "🙃",
        "winking_face": "😉",
        "smiling_face_smiling_eyes": "😊",
        "smiling_face_halo": "😇",
        "smiling_face_hearts": "🥰",
        "smiling_face_heart_eyes": "😍",
        "star_struck": "🤩",
        "face_blowing_kiss": "😘",
        "kissing_face": "😗",
        "kissing_face_closed_eyes": "😚",
        "kissing_face_smiling_eyes": "😙",
        "face_savoring_food": "😋",
        "face_tongue": "😛",
        "winking_face_tongue": "😜",
        "zany_face": "🤪",
        "squinting_face_tongue": "😝",
        "money_mouth_face": "🤑",
        "hugging_face": "🤗",
        "face_hand_over_mouth": "🤭",
        "shushing_face": "🤫",
        "thinking_face": "🤔",
        "zipper_mouth_face": "🤐",
        "face_raised_eyebrow": "🤨",
        "neutral_face": "😐",
        "expressionless_face": "😑",
        "face_without_mouth": "😶",
        "smirking_face": "😏",
        "unamused_face": "😒",
        "face_rolling_eyes": "🙄",
        "grimacing_face": "😬",
        "lying_face": "🤥",
        "relieved_face": "😌",
        "pensive_face": "😔",
        "sleepy_face": "😪",
        "drooling_face": "🤤",
        "sleeping_face": "😴",
        "face_medical_mask": "😷",
        "face_thermometer": "🤒",
        "face_head_bandage": "🤕",
        "nauseated_face": "🤢",
        "face_vomiting": "🤮",
        "sneezing_face": "🤧",
        "hot_face": "🥵",
        "cold_face": "🥶",
        "woozy_face": "🥴",
        "dizzy_face": "😵",
        "exploding_head": "🤯",
        "cowboy_hat_face": "🤠",
        "partying_face": "🥳",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "action": "🎯"
    }



        # self.logo = "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛🟩⬛⬛⬛⬛🟨🟨🟨⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛🟩🟩⬛🟩🟨⬛🟨⬛⬛⬜⬛⬛⬜⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛🟩🟩⬛🟩🟨⬛🟨⬛⬛⬜⬛⬛⬜⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛🟩🟩⬛🟩🟨⬛🟨⬛⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛🟩🟩⬛🟩🟨⬛🟨🟨⬛⬜⬛⬛⬜⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛🟩🟩🟩⬛⬛⬛🟨⬜⬜⬛⬛⬜⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n" + \
        #     "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"


    def __call__(self, text, level, end=False):
        emoji = self.emoji_dict.get(level.lower(), "")
        return f"{emoji}  {text}" if not end else f"{text}  {emoji}"

