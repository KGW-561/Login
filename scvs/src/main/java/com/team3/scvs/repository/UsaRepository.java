package com.team3.scvs.repository;

import com.team3.scvs.entity.UsaEntity;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UsaRepository extends JpaRepository<UsaEntity, Long> {
    @Query("SELECT u FROM UsaEntity u ORDER BY u.usaEconNewsId DESC, u.publishedAt DESC")
    List<UsaEntity> findTop5ByOrderByUsaEconNewsIdDescPublishedAtDesc(Pageable pageable);
}
