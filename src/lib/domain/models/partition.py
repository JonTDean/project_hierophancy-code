from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, Set, Optional, List, cast, FrozenSet
from src.lib.domain.types.nodes import NodeLike, BaseNode
from src.lib.domain.types.general import CommunityId

@dataclass
class Partition:
    node2com: Dict[NodeLike, CommunityId]

    def __post_init__(self) -> None:
        self.com2nodes: Dict[CommunityId, Set[NodeLike]] = defaultdict(set)
        for n, c in self.node2com.items():
            self.com2nodes[c].add(n)

    def communities(self) -> List[Set[NodeLike]]:
        return [set(s) for s in self.com2nodes.values() if s]

    def community_ids(self) -> List[CommunityId]:
        return [cid for cid, nodes in self.com2nodes.items() if nodes]

    def size(self) -> int:
        return sum(1 for nodes in self.com2nodes.values() if nodes)

    def community_of(self, v: NodeLike) -> CommunityId:
        return self.node2com[v]

    def members(self, cid: CommunityId) -> Set[NodeLike]:
        return self.com2nodes[cid]

    def is_singleton(self, v: NodeLike) -> bool:
        cid = self.community_of(v)
        return len(self.com2nodes[cid]) == 1

    def new_community_id(self) -> CommunityId:
        base = "__C__"
        k = 0
        while (base + str(k)) in self.com2nodes:
            k += 1
        return base + str(k)

    def move(self, v: NodeLike, dest: Optional[CommunityId]) -> CommunityId:
        src = self.node2com[v]
        if dest is None:
            dest = self.new_community_id()
        if src == dest:
            return dest
        self.com2nodes[src].remove(v)
        self.com2nodes[dest].add(v)
        self.node2com[v] = dest
        return dest

    def drop_empty(self) -> None:
        empty = [cid for cid, nodes in self.com2nodes.items() if not nodes]
        for cid in empty:
            del self.com2nodes[cid]

    def flattened_partition(self) -> List[Set[BaseNode]]:
        def expand(node: NodeLike | object) -> Set[BaseNode]:
            if isinstance(node, frozenset):
                out: Set[BaseNode] = set()
                for x in cast(FrozenSet[NodeLike], node):
                    out |= expand(x)
                return out
            # node is a BaseNode (hashable)
            return {cast(BaseNode, node)}
        out: List[Set[BaseNode]] = []
        for cid in self.community_ids():
            base_union: Set[BaseNode] = set()
            for n in self.members(cid):
                base_union |= expand(n)
            if base_union:
                out.append(base_union)
        return out