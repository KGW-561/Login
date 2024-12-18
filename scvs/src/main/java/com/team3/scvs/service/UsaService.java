package com.team3.scvs.service;

import com.team3.scvs.dto.UsaDTO;
import com.team3.scvs.entity.UsaEntity;
import com.team3.scvs.repository.UsaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UsaService {
    private final UsaRepository usaRepository;

    //뉴스 목록 조회
    public Page<UsaDTO> getUsaList(Pageable pageable) {
        int page = pageable.getPageNumber() - 1; //실제 사용자가 요청한 페이지 값에서 하나 뺀 값 (page 인덱스는 0부터 시작)
        int pageLimit = 5; //한 페이지에 보여줄 기사 개수

        //최근 기사부터 내림차순 정렬
        Page<UsaEntity> usaEntities = usaRepository.findAll(PageRequest.of(page, pageLimit, Sort.by(Sort.Direction.DESC, "usaEconNewsId")));

        //map 메소드를 이용하여 엔티티를 dto 객체로 바꿔서 반환
        return usaEntities.map(usa -> new UsaDTO(
                usa.getUsaEconNewsId(),
                usa.getTitle(),
                usa.getSource(),
                usa.getPublishedAt(),
                usa.getImageLink()));

    }

    //뉴스 상세 페이지 조회
    public UsaDTO findById(Long usaEconNewsId) {
        //주어진 usaEconNewsId로 엔티티 조회
        Optional<UsaEntity> optionalUsaEntity = usaRepository.findById(usaEconNewsId);

        if (optionalUsaEntity.isPresent()) {//데이터가 존재하면
            //엔티티 객체를 UsaEntity 타입 변수에 저장
            UsaEntity usaEntity = optionalUsaEntity.get();

            //엔티티를 dto 객체로 바꿔서 반환
            return UsaDTO.toUsaDto(usaEntity);

        } else {//데이터가 존재하지 않으면
            return null;

        }

    }

    public List<UsaDTO> getMainHomeNews(){
        List<UsaEntity> mainNews = usaRepository.findTop5ByOrderByUsaEconNewsIdDescPublishedAtDesc(PageRequest.of(0, 5));
        return mainNews.stream().map(usa -> new UsaDTO(
                usa.getUsaEconNewsId(),
                usa.getTitle(),
                usa.getSource(),
                usa.getPublishedAt(),
                usa.getImageLink()
        )).toList();
    }
}
