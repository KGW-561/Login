package com.team3.scvs.service;

import com.team3.scvs.dto.*;
import com.team3.scvs.entity.CommunityCommentViewEntity;
import com.team3.scvs.entity.CommunityEntity;
import com.team3.scvs.entity.CommunityStockInfoEntity;

import com.team3.scvs.entity.StockNewsEntity;
import com.team3.scvs.repository.*;
import com.team3.scvs.util.ConvertUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class StocksService {

    private final CommunityStockInfoRepository communityStockInfoRepository;
    private final StocksRepository stocksRepository;
    private final CommunityCommentViewRepository commentViewRepository;
    private final CommunityRepository communityRepository;
    private final StockNewsRepository stockNewsRepository;

    //주식 기초 정보
    public CommunityStockInfoDTO getStockInfo(Long tickerId) {
        // 엔티티 조회
        CommunityStockInfoEntity entity = communityStockInfoRepository.findById(tickerId).orElse(null);
        // 엔티티가 존재하지 않으면 null 반환
        if (entity == null) {
            return null;
        }
        // DTO로 변환하여 반환
        return ConvertUtil.convertToDTO(entity);
    }

    // 주식에 다양한 정보
    public Optional<StocksDTO> getStocksInfo(Long tickerId) {
        return stocksRepository.findByTickerId(tickerId).map(ConvertUtil::convertToDTO);
    }

    //뉴스 리스트 조회
    public Page<StockNewsDTO> getStockNewsList(Long tickerId, Pageable pageable) {
        int page = pageable.getPageNumber() - 1; //실제 사용자가 요청한 페이지 값에서 하나 뺀 값 (page 인덱스는 0부터 시작)
        int pageLimit = 3; //한 페이지에 보여줄 기사 개수

        Page<StockNewsEntity> stockNewsEntities = stockNewsRepository.findByTickerId
                (tickerId,PageRequest.of(page, pageLimit, Sort.by(Sort.Direction.DESC, "publishedAt")));

        // map 메서드를 이용해 ConvertUtil의 convertToDTO를 사용하여 변환
        return stockNewsEntities.map(ConvertUtil::convertToDTO);
    }

    //뉴스 상세 페이지 조회
    public StockNewsDTO findById(String stockNewsId, Long tickerId) {
        //주어진 stockNewsId로 엔티티 조회
        Optional<StockNewsEntity> optionalStockNewsEntity = stockNewsRepository.findById(stockNewsId);

        if (optionalStockNewsEntity.isPresent() && optionalStockNewsEntity.get().getTickerId() == tickerId) {//데이터가 존재하고 티커 아이디가 일치하는 경우
            //엔티티를 dto 객체로 바꿔서 반환
            return ConvertUtil.convertToDTO(optionalStockNewsEntity.get());

        } else {//데이터가 존재하지 않으면
            return null;

        }

    }

    public CommunityDTO getOrCreateCommunity(Long tickerId) {
        // tickerId로 CommunityEntity 조회
        CommunityEntity community = communityRepository.findByTickerId(tickerId).orElse(null);

        if (community == null) {
            // 조회 결과가 없으면 새 엔티티 생성
            CommunityEntity newCommunity = new CommunityEntity();
            newCommunity.setTickerId(tickerId); // tickerId 설정
            community = communityRepository.save(newCommunity); // 저장 후 반환
        }

        // convertToDTO 메서드를 사용하여 CommunityDTO로 변환
        return ConvertUtil.convertToDTO(community);
    }

    // 특정 communityId에 대한 최신 댓글 가져오기
    public CommunityCommentViewDTO getLatestComment(long communityId) {
        CommunityCommentViewEntity entity = commentViewRepository
                .findTopByCommunityIdOrderByPublishedAtDesc(communityId)
                .orElse(null); // 댓글이 없으면 null 반환
        // entity가 null일 경우 기본 메시지 반환
        if (entity == null) {
            // 댓글이 없을 때 기본값 반환
            return new CommunityCommentViewDTO(
                    0L,                   // id
                    0L,                      // userId
                    communityId,             // communityId
                    "시스템",                // nickname
                    "최신 댓글이 없습니다.", // comment
                    null,                    // publishedAt
                    null,                    // updatedAt
                    "방금"                   // timeAgo
            );
        }
        return ConvertUtil.convertToDTO(entity);
    }
    // 특정 communityId에 대한 전체 댓글 수 가져오기
    public long getTotalComments(long communityId) {
        return commentViewRepository.countByCommunityId(communityId);
    }
}
