class Emotes():
    @staticmethod
    def count(emotes_tag: str) -> int:
        if not emotes_tag:
            return
        
        emote_count = 0
        parts = emotes_tag.split('/')

        for part in parts:
            if ':' in part:
                emote_range = part.split(':')[1]
                emote_count += len(emote_range.split(','))

        return emote_count

    @staticmethod
    def remove_from_message(content: str, emotes_tag: str) -> str:
        if not emotes_tag:
            return content

        ranges = []

        for emote in emotes_tag.split('/'):
            positions = emote.split(':')[1]
            
            for pos in positions.split(','):
                start, end = map(int, pos.split('-'))
                ranges.append((start, end))

        for start, end in sorted(ranges, reverse=True):
            content = content[:start] + content[end + 1:]

        return content