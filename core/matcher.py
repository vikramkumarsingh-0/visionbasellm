from typing import List, Dict

class ElementMatcher:
    @staticmethod
    def calculate_iou(box1: List[int], box2: List[int]) -> float:
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        
        if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
            return 0.0
        
        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0
    
    @staticmethod
    def match_vision_to_dom(visual_elements: List[Dict], dom_elements: List[Dict], iou_threshold: float = 0.3) -> List[Dict]:
        matched = []
        
        for vis_el in visual_elements:
            best_match = None
            best_iou = 0.0
            
            for dom_el in dom_elements:
                iou = ElementMatcher.calculate_iou(vis_el['bbox'], dom_el['bbox'])
                if iou > best_iou and iou >= iou_threshold:
                    best_iou = iou
                    best_match = dom_el
            
            if best_match:
                matched.append({
                    'visual': vis_el,
                    'dom': best_match,
                    'iou': best_iou
                })
        
        return matched
