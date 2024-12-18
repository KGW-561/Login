package com.team3.scvs.util;

import com.team3.scvs.dto.*;
import com.team3.scvs.entity.*;

public class ConvertUtil {
    // Entity -> DTO 변환 메서드
    public static CommunityStockInfoDTO convertToDTO(CommunityStockInfoEntity entity){
        return new CommunityStockInfoDTO(
                entity.getTickerId(),
                entity.getSymbol(),
                entity.getCompany(),
                entity.getMarket(),
                entity.getCurrentprice()
        );
    }


    public static CommunityVoteDTO convertToDTO(CommunityVoteEntity entity) {
        return new CommunityVoteDTO(
                entity.getCommunityVoteId(),
                entity.getCommunity().getCommunityId(),
                entity.getPositiveVotes(),
                entity.getNegativeVotes()
        );
    }

    public static CommunityDTO convertToDTO(CommunityEntity entity) {
        return new CommunityDTO(
                entity.getCommunityId(),
                entity.getTickerId()
        );
    }

    public static StocksDTO convertToDTO(StocksEntity entity) {
        return new StocksDTO(
                entity.getStockId(),
                entity.getTickerId(),
                entity.getMarket(),
                entity.getCurrentPrice(),
                entity.getClose(),
                entity.getOpen(),
                entity.getVolume(),
                entity.getFiftytwoWeekLow(),
                entity.getFiftytwoWeekHigh(),
                entity.getDayLow(),
                entity.getDayHigh(),
                entity.getReturnOnAssets(),
                entity.getReturnOnEquity(),
                entity.getEnterpriseValue(),
                entity.getEnterpriseToEBITDA(),
                entity.getPriceToBook(),
                entity.getPriceToSales(),
                entity.getEarningsPerShare(),
                entity.getCurrentRatio(),
                entity.getDebtToEquity()
        );
    }

    public static StockNewsTitleDTO convertToDTO(StockNewsTitleEntity entity) {
        return new StockNewsTitleDTO(
                entity.getId(),
                entity.getTitle(),
                entity.getTickerId(),
                entity.getSentiment(),
                entity.getPublishedAt(),
                entity.getMarket()
        );
    }
    public static CommunityCommentViewDTO convertToDTO(CommunityCommentViewEntity entity) {
        return new CommunityCommentViewDTO(
                entity.getId(),
                entity.getUserId(),
                entity.getCommunityId(),
                entity.getNickname(),
                entity.getComment(),
                entity.getPublishedAt(),
                entity.getUpdatedAt(),
                entity.getTimeAgo()
        );
    }
  
    public static StockNewsDTO convertToDTO(StockNewsEntity entity) {
        return StockNewsDTO.builder()
                .stockNewsId(entity.getStockNewsId())
                .title(entity.getTitle())
                .source(entity.getSource())
                .imageLink(entity.getImageLink())
                .content(entity.getContent())
                .sentiment(entity.getSentiment())
                .publishedAt(entity.getPublishedAt())
                .link(entity.getLink())
                .tickerId(entity.getTickerId())
                .market(entity.getMarket())
                .build();
    }

    // convert (UserEntity >> UserDTO)
    public static UserDTO convertToDTO(UserEntity userEntity) {
        UserDTO userDTO = new UserDTO();
        userDTO.setEmail(userEntity.getEmail());
        userDTO.setNickname(userEntity.getNickname());
        userDTO.setUserrole(userEntity.getUserrole());
        userDTO.setUserId(userEntity.getUserId());
        return userDTO;
    }

    public static PSADTO convertToDTO(PSAEntity psaEntity) {
        return new PSADTO(
                psaEntity.getId(),
                psaEntity.getTitle(),
                psaEntity.getContent(),
                psaEntity.getPublishedAt()
        );
    }

    public static PSAEntity convertToEntity(PSADTO psaDTO) {
        return new PSAEntity(
                psaDTO.getId(),
                psaDTO.getTitle(),
                psaDTO.getContent(),
                psaDTO.getPublishedAt()
        );
    }
}
