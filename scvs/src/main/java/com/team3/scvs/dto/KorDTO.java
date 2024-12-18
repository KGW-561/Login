package com.team3.scvs.dto;

import com.team3.scvs.entity.KorEntity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class KorDTO {
    private Long korEconNewsId;
    private String title;
    private String source;
    private String imageLink;
    private String content;
    private LocalDateTime publishedAt;
    private String link;

    //뉴스 리스트 생성자
    public KorDTO(Long korEconNewsId, String title, String source, LocalDateTime publishedAt, String imageLink) {
        this.korEconNewsId = korEconNewsId;
        this.title = title;
        this.source = source;
        this.publishedAt = publishedAt;
        this.imageLink = imageLink;

    }

    //엔티티를 dto로 변환
    public static KorDTO toKorDto(KorEntity korEntity) {
        KorDTO korDto = new KorDTO();

        korDto.setKorEconNewsId(korEntity.getKorEconNewsId());
        korDto.setTitle(korEntity.getTitle());
        korDto.setSource(korEntity.getSource());
        korDto.setImageLink(korEntity.getImageLink());
        korDto.setContent(korEntity.getContent());
        korDto.setPublishedAt(korEntity.getPublishedAt());
        korDto.setLink(korEntity.getLink());

        return korDto;

    }

}
