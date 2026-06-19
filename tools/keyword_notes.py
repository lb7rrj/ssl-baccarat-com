from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例配置数据
SAMPLE_URL = "https://ssl-baccarat.com"
SAMPLE_KEYWORD = "百家乐"

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def short_summary(self, max_len: int = 60) -> str:
        truncated_note = (self.note[:max_len] + '...') if len(self.note) > max_len else self.note
        return f"[{self.keyword}] {truncated_note}"

    def formatted_entry(self, separator: str = " | ") -> str:
        tags_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"{self.keyword}{separator}{self.source_url}{separator}{self.note}{separator}[{tags_str}]"


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.keyword == keyword]

    def find_by_url(self, url_fragment: str) -> List[KeywordNote]:
        return [n for n in self.notes if url_fragment in n.source_url]

    def format_all(self, separator: str = " | ") -> str:
        if not self.notes:
            return "暂无笔记。"
        lines = []
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.formatted_entry(separator)}")
        return "\n".join(lines)

    def export_as_csv(self, delimiter: str = ",") -> str:
        header = delimiter.join(["序号", "关键词", "来源URL", "笔记", "标签", "创建时间"])
        rows = [header]
        for i, note in enumerate(self.notes, 1):
            safe_note = note.note.replace("\"", "\"\"")
            tags_str = "; ".join(note.tags)
            row = delimiter.join([
                str(i),
                note.keyword,
                note.source_url,
                f"\"{safe_note}\"",
                tags_str,
                note.created_at or ""
            ])
            rows.append(row)
        return "\n".join(rows)


def generate_demo_notes() -> KeywordNoteCollection:
    collection = KeywordNoteCollection()
    collection.add_note(KeywordNote(
        keyword=SAMPLE_KEYWORD,
        source_url=SAMPLE_URL,
        note="一条关于百家乐游戏规则与策略的基础笔记。",
        tags=["规则", "策略", "入门"]
    ))
    collection.add_note(KeywordNote(
        keyword=SAMPLE_KEYWORD,
        source_url=f"{SAMPLE_URL}/strategy",
        note="百家乐高级策略分析，包括庄闲概率与投注管理。",
        tags=["高级", "概率", "资金管理"]
    ))
    collection.add_note(KeywordNote(
        keyword="扑克",
        source_url="https://example.com/poker",
        note="扑克与百家乐在概率计算上有相似之处。",
        tags=["类比", "概率"]
    ))
    return collection


def main():
    print("===== 关键词笔记演示 =====")
    print(f"示例URL: {SAMPLE_URL}")
    print(f"核心关键词: {SAMPLE_KEYWORD}\n")

    collection = generate_demo_notes()
    print("--- 格式化输出所有笔记 ---")
    print(collection.format_all())

    print("\n--- 查找关键词为『百家乐』的笔记 ---")
    baccarat_notes = collection.find_by_keyword(SAMPLE_KEYWORD)
    for note in baccarat_notes:
        print(note.short_summary())

    print("\n--- 查找URL包含 baccarat 的笔记 ---")
    url_notes = collection.find_by_url("baccarat")
    for note in url_notes:
        print(note.formatted_entry())

    print("\n--- CSV 导出预览 ---")
    csv_output = collection.export_as_csv()
    print(csv_output)


if __name__ == "__main__":
    main()