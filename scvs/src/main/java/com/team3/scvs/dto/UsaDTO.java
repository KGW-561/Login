package com.team3.scvs.dto;

import lombok.*;
import java.time.LocalDateTime;
import com.team3.scvs.entity.UsaEntity;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class UsaDTO {
    private Long usaEconNewsId;
    private String title;
    private String source;
    private String imageLink;
    private String content;
    private LocalDateTime publishedAt;
    private String link;

    //뉴스 리스트 생성자
    public UsaDTO(Long usaEconNewsId, String title, String source, LocalDateTime publishedAt, String imageLink) {
        this.usaEconNewsId = usaEconNewsId;
        this.title = title;
        this.source = source;
        this.publishedAt = publishedAt;
        this.imageLink = imageLink;

    }

    //엔티티를 dto로 변환
    public static UsaDTO toUsaDto(UsaEntity usaEntity) {
        UsaDTO usaDto = new UsaDTO();

        usaDto.setUsaEconNewsId(usaEntity.getUsaEconNewsId());
        usaDto.setTitle(usaEntity.getTitle());
        usaDto.setSource(usaEntity.getSource());
        usaDto.setImageLink(usaEntity.getImageLink());
        usaDto.setContent(usaEntity.getContent());
        usaDto.setPublishedAt(usaEntity.getPublishedAt());
        usaDto.setLink(usaEntity.getLink());

        return usaDto;

    }

}
